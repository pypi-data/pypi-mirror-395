import logging
from collections import defaultdict, OrderedDict
from enum import Enum
from itertools import groupby, chain
from typing import Type, cast, List, Optional, Dict

from collections_extended import RangeMap, MappedRange
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation, AltText

logger = Logger("pymultirole")


class WrappedTerm(object):
    def __init__(self, term):
        self.term = term
        self.status = term.properties.get('status', "") if term.properties else ""

    def __eq__(self, other):
        return self.term.identifier == other.term.identifier and self.status == other.status

    def __hash__(self):
        return hash((self.term.identifier, self.status))


class ConsolidationType(str, Enum):
    linker = "linker"
    ref_first = "ref_first"


class AFPEntitiesParameters(ProcessorParameters):
    type: ConsolidationType = Field(
        ConsolidationType.linker,
        description="""Type of consolidation, use<br />
    <li>**default** deduplicate and if overlap keeps only the longest match<br />
    <li>**linker** to retain only known entities<br />
    <li>**candidate** to retain all known entities and keeping the unknown as candidates<br />""",
        extra="advanced",
    )
    kill_label: Optional[str] = Field("kill", description="Label name of the kill list")
    white_label: Optional[str] = Field(
        "white", description="Label name of the white list"
    )
    eurovoc_label: Optional[str] = Field(
        "eurovoc", description="Label name of the Eurovoc thesaurus"
    )
    wikidata_label: Optional[str] = Field(
        "wikidata", description="Label name of Wikidata entities"
    )
    as_altText: str = Field(
        "fingerprint",
        description="""If defined generate the fingerprint as an alternative text of the input document.""",
    )
    remove_suspicious: bool = Field(
        True,
        description="Remove suspicious annotations extracted by the model (numbers, percentages, phrases without uppercase words)",
    )
    resolve_lastnames: bool = Field(
        False,
        description="Try to resolve isolated family names if they have been seen before in the document",
    )


class AFPEntitiesProcessor(ProcessorBase):
    """AFPEntities processor ."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: AFPEntitiesParameters = cast(AFPEntitiesParameters, parameters)
        for document in documents:
            with add_logging_context(docid=document.identifier):
                if document.annotations:
                    annotations = [a for a in document.annotations if a.labelName != 'sentence']
                    mark_whitelisted(annotations, params.white_label)
                    ann_groups = group_annotations(annotations, keyfunc=by_lexicon)
                    # 1. Compute document fingerprint
                    fingerprints = compute_fingerprint(ann_groups)
                    if params.as_altText is not None and len(params.as_altText):
                        document.altTexts = document.altTexts or []
                        altTexts = [
                            alt
                            for alt in document.altTexts
                            if alt.name != params.as_altText
                        ]
                        altTexts.append(
                            AltText(name=params.as_altText, text=" ".join(fingerprints))
                        )
                        document.altTexts = altTexts
                    # 2. Consolidate & links against KB and Wikidata
                    if params.type == ConsolidationType.linker:
                        conso_anns = consolidate_linker(
                            ann_groups,
                            params
                        )
                    else:
                        conso_anns = consolidate_candidate(
                            document.text,
                            ann_groups,
                            params
                        )
                    document.annotations = [a for a in conso_anns if
                                            a.labelName not in ["witness", 'loc_org', 'signature']]
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AFPEntitiesParameters


EUROVOC_NS = "http://eurovoc.europa.eu/"


def compute_fingerprint(ann_groups):
    def get_sort_key(r: MappedRange):
        return -r.start, r.stop - r.start

    fingerprints = []
    sorted_ann = sorted(
        chain(ann_groups["wikidata"].ranges(), ann_groups["eurovoc"].ranges()),
        key=get_sort_key,
        reverse=True,
    )
    for r in sorted_ann:
        ann = r.value
        if ann.terms and len(ann.terms):
            if ann.terms[0].lexicon == "wikidata":
                fingerprints.append(ann.terms[0].identifier)
                fingerprint = ann.terms[0].properties.get("fingerprint", None)
                if fingerprint:
                    props_vals = [
                        (p, v)
                        for p, v in [
                            pv.split(":", maxsplit=1) for pv in fingerprint.split(",")
                        ]
                    ]
                    ann.terms[0].properties["fingerprint"] = props_vals
                    try:
                        fingerprints.extend(
                            [v for p, v in props_vals if v.startswith("Q")]
                        )
                    except BaseException:
                        logging.exception()
            elif ann.terms[0].lexicon == "eurovoc":
                for t in ann.terms:
                    if t.identifier.startswith(EUROVOC_NS):
                        fingerprints.append("E" + t.identifier[len(EUROVOC_NS):])
    return fingerprints


def mark_whitelisted(annotations, white_label):
    for a in annotations:
        if (
                a.labelName == white_label
        ):  # Consider whitelisted terms as entities coming from the model
            a.terms = None


def consolidate_linker(
        ann_groups,
        params: AFPEntitiesParameters
):
    conso_anns = []
    kb_names = [
        item
        for item in ann_groups.keys()
        if item not in ["", params.kill_label, params.white_label, params.wikidata_label, params.eurovoc_label]
    ]
    for model_r in ann_groups[""].ranges():
        model_ann = model_r.value
        gname = model_ann.labelName

        if params.remove_suspicious and is_suspicious(model_ann):
            logger.warning("Kill suspicious annotation")
            logger.warning(f"=> {model_ann}")
            continue
        kill_r = annotation_in_group(model_ann, ann_groups, [params.kill_label])
        perfect, kill_match = one_match(model_ann, kill_r)
        if perfect and kill_match:
            logger.warning("Kill annotation")
            logger.warning(f"=> {model_ann}")
            continue

        kb_r = annotation_in_group(model_ann, ann_groups, kb_names)
        perfect, kb_match = one_match(model_ann, kb_r)
        if kb_match:
            if perfect:
                model_ann.labelName = kb_match.labelName
                model_ann.label = kb_match.label
                model_ann.terms = model_ann.terms or []
                model_ann.terms.extend(kb_match.terms)
            else:
                logger.warning("Found larger annotation in KB")
                logger.warning(f"=> {model_ann}")
                logger.warning("and")
                logger.warning(f" -{kb_match}")
        elif kb_r and len(kb_r) > 1:
            logger.warning("Found overlapping annotations in KB")
            logger.warning(f"=> {model_ann}")
            logger.warning("and")
            for r in kb_r.values():
                logger.warning(f" -{r}")

        wiki_r = annotation_in_group(model_ann, ann_groups, [params.wikidata_label])
        perfect, wiki_match = one_match(model_ann, wiki_r)
        if wiki_match:
            if validate_wiki_type(wiki_match, gname):
                if perfect:
                    model_ann.terms = model_ann.terms or []
                    wiki_match.terms[0].properties.pop("fingerprint", None)
                    model_ann.terms.extend(wiki_match.terms)
                else:
                    logger.warning("Found larger annotation in Wikidata")
                    logger.warning(f"=> {model_ann}")
                    logger.warning("and")
                    logger.warning(f" -{wiki_match}")
        elif wiki_r and len(wiki_r) > 1:
            logger.warning("Found overlapping annotations in Wikidata")
            logger.warning(f"=> {model_ann}")
            logger.warning("and")
            for r in wiki_r.values():
                logger.warning(f" -{r}")
        conso_anns.append(model_ann)
    return conso_anns


def has_knowledge(a: Annotation):
    return a.terms is not None and a.terms


def consolidate_candidate(
        text,
        ann_groups,
        params: AFPEntitiesParameters
):
    ordered_labels = [params.kill_label,
                      'afpperson', 'afplocation', 'afporganization',
                      'person', 'location', 'organization',
                      'loc_org', 'witness', params.white_label, params.wikidata_label,
                      params.eurovoc_label]

    def get_sort_key(a: Annotation):
        lab = a.labelName
        label_index = ordered_labels.index(lab) if lab in ordered_labels else 100
        return a.end - a.start, -a.start, -label_index

    sorted_annotations = sorted(
        chain(ann_groups["kill"].values(),
              ann_groups["person"].values(),
              ann_groups["location"].values(),
              ann_groups["organization"].values(),
              ann_groups[""].values()
              ),
        key=get_sort_key,
        reverse=True,
    )
    seen_offsets = RangeMap()
    conso_anns = defaultdict(list)
    for ann in sorted_annotations:
        if params.remove_suspicious and is_suspicious(ann):
            logger.warning("Kill suspicious annotation")
            logger.warning(f"=> {ann}")
            continue
        alex = by_lexicon(ann)
        if (
                seen_offsets.get(ann.start) is None
                and seen_offsets.get(ann.end - 1) is None
        ):
            if ann.labelName not in [params.kill_label, params.white_label]:
                conso_anns[(ann.start, ann.end)].append(ann)
            seen_offsets[ann.start: ann.end] = ann
        else:
            target = seen_offsets.get(ann.start) or seen_offsets.get(ann.end - 1)
            if target.labelName != params.kill_label and target.labelName != params.white_label:
                if target.start - ann.start == 0 and target.end - ann.end == 0:
                    if ann.score is not None and ann.score > 0.0:
                        target.score = ann.score
                    tlex = by_lexicon(target)
                    if tlex in ['person', 'location',
                                'organization']:  # target is an AFP entity
                        # The AFP entity is a person and the model entity a witness => keep the AFP
                        if tlex == 'person' and ann.labelName == 'witness':
                            pass
                        # The AFP entity is ambiguous, keep it and try to disambiguate later thanks to the model
                        elif alex in ['person', 'location',
                                      'organization']:
                            conso_anns[(ann.start, ann.end)].append(ann)
                        # The AFP entity and the model entity have different types => disambiguate or keep the model
                        elif alex == '':
                            # If whitelist, keep all, else try to disambiguate using model type
                            if ann.labelName != params.white_label:
                                disambs = []
                                for a in conso_anns[(ann.start, ann.end)]:
                                    tlex = by_lexicon(a)
                                    if ann.labelName == tlex:
                                        disambs.append(a)
                                if not disambs:
                                    disambs = [ann]
                                conso_anns[(ann.start, ann.end)] = disambs

    sorted_annotations = sorted([item for sublist in conso_anns.values() for item in sublist],
                                key=natural_order,
                                reverse=True,
                                )

    seen_names = defaultdict(set)
    for ann in sorted_annotations:
        # Link to wikidata
        wiki_r = annotation_in_group(ann, ann_groups, [params.wikidata_label])
        perfect, wiki_match = one_match(ann, wiki_r)
        if wiki_match:
            gname = by_lexicon_or_label(ann)
            if validate_wiki_type(wiki_match, gname):
                if perfect:
                    ann.terms = ann.terms or []
                    wiki_match.terms[0].properties.pop("fingerprint", None)
                    ann.terms.extend(wiki_match.terms)
                else:
                    logger.warning("Found larger annotation in Wikidata")
                    logger.warning(f"=> {ann}")
                    logger.warning("and")
                    logger.warning(f" -{wiki_match}")
        elif wiki_r and len(wiki_r) > 1:
            logger.warning("Found overlapping annotations in Wikidata")
            logger.warning(f"=> {ann}")
            logger.warning("and")
            for r in wiki_r.values():
                logger.warning(f" -{r}")
        # Resolve incomplete person names
        if params.resolve_lastnames:
            lastnames = person_varnames(ann, text)
            if lastnames is not None:
                for composed_name in lastnames:
                    if len(lastnames) > 1:
                        if has_knowledge(ann):
                            for t in ann.terms:
                                seen_names[composed_name].add(WrappedTerm(t))
                        else:
                            seen_names[composed_name].add(None)
                    elif ann.labelName == 'person':
                        if composed_name in seen_names:
                            ann.terms = [wt.term for wt in seen_names[composed_name] if wt is not None]
                            if any([t.identifier.startswith('afp') for t in ann.terms]):
                                ann.labelName = 'afpperson'
                                ann.label = "AFPPerson"
                            break
    return sorted_annotations


def group_annotations(annotations, keyfunc):
    groups = defaultdict(RangeMap)
    sorted_annotations = sorted(annotations, key=keyfunc)
    for k, g in groupby(sorted_annotations, keyfunc):
        sorted_group = sorted(g, key=left_longest_match, reverse=True)
        for a in sorted_group:
            addit = True
            if a.start in groups[k] and a.end - 1 in groups[k]:
                aterms = set(WrappedTerm(t) for t in a.terms) if a.terms else set()
                a_hasX = next(filter(lambda wt: wt.status == 'X', aterms), False)
                b = groups[k][a.start]
                bterms = set(WrappedTerm(t) for t in b.terms) if b.terms else set()
                b_hasX = next(filter(lambda wt: wt.status == 'X', bterms), False)
                addit = a_hasX or b_hasX
                if a.start - b.start == 0 and a.end - b.end == 0:
                    terms = set(WrappedTerm(t) for t in b.terms) if b.terms else set()
                    if a.terms:
                        terms.update(set(WrappedTerm(t) for t in a.terms))
                    b.terms = [t.term for t in terms]
                    addit = False
            if addit:
                groups[k][a.start:a.end] = a
        if k in ['person', 'location', 'organization']:
            to_delete = []
            for r in groups[k].ranges():
                a = r.value
                wterms = [WrappedTerm(t) for t in a.terms]
                dtermids = [wt.term.identifier for wt in wterms if wt.status == 'X']
                aterms = defaultdict(list)
                for wt in wterms:
                    if wt.term.identifier not in dtermids:
                        aterms[wt.term.identifier].append(wt.term)
                terms = []
                for tlist in aterms.values():
                    tlist = sorted(tlist, key=lambda item: item.lexicon, reverse=True)
                    terms.append(tlist[0])
                if len(terms) > 0:
                    a.terms = terms
                else:
                    to_delete.append((r.start, r.stop))
            for start, stop in to_delete:
                groups[k].delete(start=start, stop=stop)
    return groups


def left_longest_match(a: Annotation):
    return a.end - a.start, -a.start


def natural_order(a: Annotation):
    return -a.start, a.end - a.start


def is_whitelist(a: Annotation):
    if has_knowledge(a):
        for term in a.terms:
            props = term.properties or {}
            status = props.get("status", "")
            if "w" in status.lower():
                return True
    return False


def person_varnames(a: Annotation, text):
    if 'person' in a.labelName:
        atext = a.text or text[a.start:a.end]
        words = atext.split()
        if words is not None:
            variant_names = OrderedDict.fromkeys([' '.join(words[i:]) for i in range(len(words))])
            if len(words) > 1:
                variant_names2 = OrderedDict.fromkeys([' '.join(words[0:i - 1]) for i in range(2, len(words) + 1)])
                variant_names.update(variant_names2)
            return list(variant_names.keys())
    return None


def by_lexicon(a: Annotation):
    if a.terms:
        lex = a.terms[0].lexicon.split("_")
        return lex[0]
    else:
        return ""


def by_lexicon_or_label(a: Annotation):
    if a.terms:
        lex = a.terms[0].lexicon.split("_")
        return lex[0]
    else:
        return a.labelName


def by_label(a: Annotation):
    return a.labelName


def one_match(a: Annotation, matches: RangeMap):
    match = None
    perfect = False
    if matches and len(matches) >= 1:
        for match in matches.values():
            perfect = a.start == match.start and a.end == match.end
            if perfect:
                break
    return perfect, match


def is_suspicious(a: Annotation):
    suspicious = False
    if a.text:
        words = a.text.split()
        has_upper = any([w[0].isupper() for w in words])
        suspicious = not has_upper
    return suspicious


# noqa: W503
def annotation_in_group(
        a: Annotation, ann_groups: Dict[str, RangeMap], gnames: List[str] = None
):
    gname = by_lexicon_or_label(a)
    if gname in gnames:
        gnames = [gname]
    for gname in gnames:
        if (
                gname in ann_groups
                and a.start in ann_groups[gname]
                or a.end in ann_groups[gname]
        ):
            return ann_groups[gname][a.start: a.end]
    return None


# noqa
def validate_wiki_type(w: Annotation, gname: str):
    match = None
    if w.terms and len(w.terms) and w.terms[0].properties:
        fingerprint = w.terms[0].properties.get("fingerprint", None)
        if fingerprint:
            if gname == "person":
                match = next(
                    filter(lambda pv: pv[0] == "P31" and pv[1] == "Q5", fingerprint),
                    None,
                )
            elif gname == "location":
                match = next(filter(lambda pv: pv[0] == "P1566", fingerprint), None)
            elif gname == "organization":
                match = next(
                    filter(
                        lambda pv: (pv[0] == "P452")
                                   or (
                                           pv[0] == "P31"
                                           and pv[1]
                                           in [
                                               "Q6881511",
                                               "Q4830453",
                                               "Q891723",
                                               "Q484652",
                                               "Q43229",
                                               "Q245065",
                                               "Q7210356",
                                               "Q2085381",
                                               "Q11691",
                                               "Q161726",
                                               "Q484652",
                                               "Q4120211",
                                               "Q748720",
                                               "Q11422536",
                                               "Q29300714",
                                               "Q15911314",
                                               "Q17127659",
                                               "Q1788992",
                                               "Q327333",
                                               "Q15991290",
                                               "Q163740",
                                               "Q4438121",
                                               "Q1530022",
                                               "Q20746389",
                                               "Q48204",
                                               "Q207320",
                                               "Q7278",
                                               "Q875538",
                                               "Q3918",
                                               "Q14350",
                                               "Q15265344",
                                               "Q11033",
                                               "Q3778417"
                                           ]
                                   ),
                        fingerprint,
                    ),
                    None,
                )
    if not match:
        logger.warning(f"Wikidata annotation discarded as {gname}")
        logger.warning(f"=> {w}")
    return match
