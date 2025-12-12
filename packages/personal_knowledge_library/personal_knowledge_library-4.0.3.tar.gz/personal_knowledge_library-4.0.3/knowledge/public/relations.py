# -*- coding: utf-8 -*-
# Copyright © 2023-present Wacom. All rights reserved.
import functools
import multiprocessing
from typing import Any, Dict, Set, Tuple, List, Callable, Optional

from tqdm import tqdm

from knowledge.public.helper import CLAIMS_TAG, PID_TAG, LABEL_TAG, QID_TAG
from knowledge.public.wikidata import LITERALS_TAG, WikidataThing
from knowledge.public.client import WikiDataAPIClient


def __relations__(thing: Dict[str, Any], wikidata: Set[str]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Extracts relations from Wikidata.
    Parameters
    ----------
    thing: Dict[str, Any]
        Wikidata thing
    wikidata: Set[str]
        Set of unique QIDs

    Returns
    -------
    qid: str
        QID of the Wikidata thing
    relations: List[Dict[str, Any]]
        Relations of the Wikidata thing
    """
    relations: List[Dict[str, Any]] = []
    for _, p_value in thing[CLAIMS_TAG].items():
        for v in p_value[LITERALS_TAG]:
            if isinstance(v, dict) and v.get("type") in {"wikibase-entityid", "wikibase-item"}:
                ref_qid = v["value"]["id"]
                prop = p_value[PID_TAG][LABEL_TAG]
                if ref_qid in wikidata:
                    relations.append(
                        {
                            "subject": {
                                "qid": thing[QID_TAG],
                            },
                            "predicate": {"pid": p_value[PID_TAG][PID_TAG], "label": prop},
                            "target": {"qid": ref_qid},
                        }
                    )
    return thing[QID_TAG], relations


def wikidata_extractor_entities(qids: Set[str]) -> Dict[str, WikidataThing]:
    """
    Extracts an entity from Wikidata.

    Parameters
    ----------
    qids: Set[str]
        Set of unique QIDs

    Returns
    -------
    wikidata_extractor: Dict[str, WikidataThing]
        Wikidata map
    """
    return {e.qid: e for e in WikiDataAPIClient.retrieve_entities(qids)}


def wikidata_relations_extractor(
    wikidata: Dict[str, WikidataThing],
    progress_relations: Optional[Callable[[int, int], None]] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """Extracts relations from Wikidata.

    Parameters
    ----------
    wikidata: Dict[str, WikidataThing]
        Wikidata map
    progress_relations: Optional[Callable[[int, int], None]] = None
        Progress callback function.

    Returns
    -------
    relations: Dict[str, List[Dict[str, Any]]]
        Relations map.
    """
    relations: Dict[str, List[Dict[str, Any]]] = {}
    qids: Set[str] = set(wikidata.keys())
    num_processes: int = min(len(wikidata), multiprocessing.cpu_count())
    ctr: int = 0
    tasks: int = len(qids)
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Wikidata thing is not support in multiprocessing
        for qid, rels in pool.map(
            functools.partial(__relations__, wikidata=qids), [e.__dict__() for e in wikidata.values()]
        ):
            relations[qid] = rels
            ctr += 1
            if progress_relations:
                progress_relations(ctr, tasks)
    return relations


def wikidata_relations_extractor_qids(
    wikidata: Dict[str, WikidataThing], qids: Set[str]
) -> Dict[str, List[Dict[str, Any]]]:
    """Extracts relations from Wikidata.

    Parameters
    ----------
    wikidata: Dict[str, WikidataThing]
        Wikidata map
    qids: Set[str]
        Set of unique QIDs

    Returns
    -------
    relations: Dict[str, List[Dict[str, Any]]]
        Relations map.
    """
    relations: Dict[str, List[Dict[str, Any]]] = {}
    num_processes: int = min(len(wikidata), multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Wikidata thing is not support in multiprocessing
        with tqdm(total=round(len(wikidata) / num_processes), desc="Check Wikidata relations.") as pbar:
            for qid, rels in pool.map(
                functools.partial(__relations__, wikidata=qids), [e.__dict__() for e in wikidata.values()]
            ):
                relations[qid] = rels
                pbar.update(1)
    return relations
