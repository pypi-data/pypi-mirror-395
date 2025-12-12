# -*- coding: utf-8 -*-
# Copyright © 2023-present Wacom. All rights reserved.
import hashlib
import math
import urllib
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Dict, List

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from knowledge import logger, __version__
from knowledge.public import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, DEFAULT_BACKOFF_FACTOR, STATUS_FORCE_LIST


# --------------------------------------- Structures -------------------------------------------------------------------
class Precision(Enum):
    """
    Precision enum for date.
    """

    BILLION_YEARS = 0
    MILLION_YEARS = 3
    HUNDREDS_THOUSAND_YEARS = 4
    TEN_THOUSAND_YEARS = 5
    MILLENIUM = 6
    CENTURY = 7
    DECADE = 8
    YEAR = 9
    MONTH = 10
    DAY = 11


class WikiDataAPIException(Exception):
    """
    WikiDataAPIException
    --------------------
    Exception thrown when accessing WikiData fails.
    """


# --------------------------------------- Tags -------------------------------------------------------------------------
CLASS_TAG: str = "class"
ALIASES_TAG: str = "aliases"
ID_TAG: str = "id"
QID_TAG: str = "qid"
PID_TAG: str = "pid"
LAST_REVID_TAG: str = "lastrevid"
MODIFIED_TAG: str = "modified"
SYNC_TIME_TAG: str = "sync"
WIKIDATA_LANGUAGE_TAG: str = "language"
LABEL_VALUE_TAG: str = "value"
LABEL_TAG: str = "label"
SUPERCLASSES_TAG: str = "superclasses"
SUBCLASSES_TAG: str = "subclasses"
CLAIMS_TAG: str = "claims"
ONTOLOGY_TYPES_TAG: str = "ontology_types"
REVISION_TAG: str = "revision"
SITELINKS_TAG: str = "sitelinks"
TITLES_TAG: str = "titles"
URLS_TAG: str = "urls"
SOURCE_TAG: str = "source"
API_LIMIT: int = 50
# --------------------------------------- API URLs ---------------------------------------------------------------------
THUMB_IMAGE_URL: str = "https://upload.wikimedia.org/wikipedia/commons/thumb/{}/{}/{}/200px-{}"
MULTIPLE_ENTITIES_API: str = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="
WIKIDATA_LDI_URL: str = "https://www.wikidata.org/wiki/Special:EntityData"
# --------------------------------------- Wikidata Properties ----------------------------------------------------------
STUDENT_OF: str = "P1066"
STUDENT: str = "P802"
INCEPTION: str = "P571"
MOVEMENT: str = "P135"
SUBCLASS_OF: str = "P279"
TITLE: str = "P1476"
COLLECTION: str = "P195"
GENRE: str = "P136"
CREATOR: str = "P170"
LOGO_IMAGE: str = "P154"
FLAG_IMAGE: str = "P41"
GREGORIAN_CALENDAR: str = "Q1985727"
START_TIME: str = "P580"
END_TIME: str = "P582"
FOLLOWS: str = "P155"
FOLLOWED_BY: str = "P156"
COUNTRY_OF_ORIGIN: str = "P495"
COUNTRY: str = "P17"
INSTANCE_OF: str = "P31"
IMAGE: str = "P18"
# URL - Wikidata
GREGORIAN_CALENDAR_URL: str = "http://www.wikidata.org/entity/Q1985786"
# URL - Wikidata service
WIKIDATA_SPARQL_URL: str = "https://query.wikidata.org/sparql"
WIKIDATA_SEARCH_URL: str = "https://www.wikidata.org/w/api.php"


def user_agent() -> str:
    """User agent."""
    return (
        f"Personal Knowledge Library(Public Knowledge Crawler)/{__version__}"
        f"(+https://github.com/Wacom-Developer/personal-knowledge-library)"
    )


# --------------------------------------- Helper functions -------------------------------------------------------------
def image_url(img: str, dpi: int = 500):
    """
    Helper to generate image URL for Wikipedia.

    Parameters
    ----------
    img: str
        Name of image
    dpi: int
        DPI of the generated URL
    Returns
    -------
    wikimedia_url: str
        URL of wikimedia
    """
    if not (50 <= dpi <= 1000):
        raise ValueError(f"DPI should bei with range of [50-1000]. Value:={dpi}")
    extension: str = ""
    conversion: str = ""
    fixed_img: str = img.replace(" ", "_")
    if fixed_img.lower().endswith("svg"):
        extension: str = ".png"
    if fixed_img.lower().endswith("tif") or fixed_img.lower().endswith("tiff"):
        extension: str = ".jpg"
        conversion: str = "lossy-page1-"
    hash_img: str = hashlib.md5(fixed_img.encode("utf-8")).hexdigest()
    url_img_part: str = urllib.parse.quote_plus(fixed_img)
    return (
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/"
        f"{hash_img[0]}/{hash_img[:2]}/{url_img_part}/{dpi}px-{conversion + url_img_part + extension}"
    )


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse date string to datetime object.
    Parameters
    ----------
    date_string: str
        Date string

    Returns
    -------
    parsed_date: datetime
        Parsed date
    """
    try:
        parsed_date = datetime.fromisoformat(date_string)
        return parsed_date
    except (TypeError, ValueError):
        date_part, _ = date_string.split("T")
        year, month, day = date_part.split("-")
        if month == "00":
            month = "01"
        if day == "00":
            day = "01"
        iso_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        try:
            parsed_date = datetime.fromisoformat(iso_date)
            return parsed_date
        except (TypeError, ValueError):
            return None


def wikidate(param: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and extract wikidata structure.
    Parameters
    ----------
    param: Dict[str, Any]
        Entities wikidata

    Returns
    -------
    result: Dict[str, Any]
        Dict with pretty print of date
    """
    time: str = param["time"]
    timezone: int = param["timezone"]
    before: int = param["before"]
    after: int = param["after"]
    precision: int = param["precision"]
    calendar_model: str = param["calendarmodel"]
    iso_encoded: Optional[str] = None
    after_christ: bool = True
    pretty: str = ""
    if calendar_model != "https://www.wikidata.org/wiki/Q1985727":
        if time.startswith("+"):
            time = time[1:]
        elif time.startswith("-"):
            time = time[1:]
            after_christ = False
        date_obj: Optional[datetime] = parse_date(date_string=time)
        if date_obj:
            if date_obj.day == 0:
                # Set the day component to 1
                date_obj = date_obj.replace(day=1)
            iso_encoded = date_obj.isoformat()
            pretty = date_obj.strftime("%Y-%m-%d")
        return {
            "time": time,
            "timezone": timezone,
            "before": before,
            "after": after,
            "precision": precision,
            "calendar-model": calendar_model,
            "pretty": pretty,
            "after-christ": after_christ,
            "iso": iso_encoded,
        }
    if time.startswith("+"):
        time = time[1:]
    elif time.startswith("-"):
        time = time[1:]
        after_christ = False
    # Probably not necessary
    date_str = time.strip()
    # Remove + sign
    if date_str[0] == "+":
        date_str = date_str[1:]
    # Remove missing month/day
    date_str = date_str.split("-00", maxsplit=1)[0]
    # Parse date
    try:
        if Precision.BILLION_YEARS.value == precision:
            pretty = date_str
        elif Precision.MILLION_YEARS.value == precision:
            pretty = date_str
        elif Precision.HUNDREDS_THOUSAND_YEARS.value == precision:
            pretty = date_str
        elif Precision.MILLENIUM.value == precision:
            pretty = date_str
        elif Precision.TEN_THOUSAND_YEARS.value == precision:
            pretty = date_str
        else:
            dt_obj: Optional[datetime] = parse_date(date_str)
            if dt_obj:
                if Precision.CENTURY.value == precision:
                    century: int = int(math.ceil(dt_obj.year / 100))
                    pretty = f"{century}th century"
                elif Precision.DECADE.value == precision:
                    pretty = f"{dt_obj.year}s{'' if after_christ else ' BC'}"
                elif Precision.YEAR.value == precision:
                    pretty = f"{dt_obj.year}{'' if after_christ else ' BC'}"
                elif Precision.MONTH.value == precision:
                    pretty = dt_obj.strftime("%B %Y")
                elif Precision.DAY.value == precision:
                    pretty = dt_obj.strftime("%-d %B %Y")
                iso_encoded = dt_obj.isoformat()
            else:
                iso_encoded = None
    except Exception as pe:
        logger.error(param)
        logger.exception(pe)

    return {
        "time": time,
        "timezone": timezone,
        "before": before,
        "after": after,
        "precision": precision,
        "calendar-model": calendar_model,
        "pretty": pretty,
        "after_christ": after_christ,
        "iso": iso_encoded,
    }


def __waiting_request__(
    entity_id: str,
    base_url: str = WIKIDATA_LDI_URL,
    timeout: int = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
) -> Dict[str, Any]:
    """
    Sena a request with retry policy.

    Parameters
    ----------
    entity_id: str
        Entity QID
    base_url: Base URL
        The base URL
    timeout:  int
        Timeout in seconds
    max_retries: int
        Maximum number of retries
    backoff_factor: float
        Backoff factor for retries.

    Returns
    -------
    result_dict: Dict[str, Any]
        Result dict
    """
    url: str = f"{base_url}/{entity_id}.json"
    # Define the retry policy
    retry_policy: Retry = Retry(
        total=max_retries,  # maximum number of retries
        backoff_factor=backoff_factor,  # factor by which to multiply the delay between retries
        status_forcelist=STATUS_FORCE_LIST,  # HTTP status codes to retry on
        respect_retry_after_header=True,  # respect the Retry-After header
    )
    header: Dict[str, str] = {"User-Agent": user_agent()}

    # Create a session and mount the retry adapter
    with requests.Session() as session:
        retry_adapter = HTTPAdapter(max_retries=retry_policy)
        session.mount("https://", retry_adapter)

        # Make a request using the session
        response: Response = session.get(url, headers=header, timeout=timeout)

        # Check the response status code
        if not response.ok:
            raise WikiDataAPIException(f"Request failed with status code : {response.status_code}. URL:= {url}")
        entity_dict_full: Dict[str, Any] = response.json()
        # remove redundant top level keys
        returned_entity_id: str = next(iter(entity_dict_full["entities"]))
        entity_dict = entity_dict_full["entities"][returned_entity_id]

        if entity_id != returned_entity_id:
            logger.warning(
                f"Wikidata redirect detected.  Input entity id={entity_id}. Returned entity id={returned_entity_id}."
            )

        return entity_dict


def __waiting_multi_request__(
    entity_ids: List[str],
    base_url: str = MULTIPLE_ENTITIES_API,
    timeout: int = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
) -> List[Dict[str, Any]]:
    """
    Sena a request to retrieve multiple entities with retry policy.

    Parameters
    ----------
    entity_ids: List[str]
        Entity QIDs
    base_url: Base URL
        The base URL
    timeout:  int
        Timeout in seconds
    max_retries: int
        Maximum number of retries
    backoff_factor: float
        Backoff factor for retries.
    Returns
    -------
    result_dict: Dict[str, Any]
        Result dict
    Raises
    ------
    ValueError - Empty list or to many entities
    """
    checked_entity_ids: List[str] = [e for e in entity_ids if e.startswith("Q")]

    if not (0 < len(checked_entity_ids) <= API_LIMIT):
        raise ValueError(
            f"Number of entities must be within [1, {API_LIMIT}]. " f"Number of QIDs: {len(checked_entity_ids)}"
        )
    query: str = "|".join(checked_entity_ids)
    url: str = f"{base_url}{query}&format=json"
    header: Dict[str, str] = {"User-Agent": user_agent()}
    # Define the retry policy
    retry_policy: Retry = Retry(
        total=max_retries,  # maximum number of retries
        backoff_factor=backoff_factor,  # factor by which to multiply the delay between retries
        status_forcelist=STATUS_FORCE_LIST,  # HTTP status codes to retry on
        respect_retry_after_header=True,  # respect the Retry-After header
    )

    # Create a session and mount the retry adapter
    with requests.Session() as session:
        retry_adapter = HTTPAdapter(max_retries=retry_policy)
        session.mount("https://", retry_adapter)

        # Make a request using the session
        response: Response = session.get(url, headers=header, timeout=timeout)

        # Check the response status code
        if not response.ok:
            raise WikiDataAPIException(f"Request failed with status code : {response.status_code}. URL:= {url}")
        entity_dict_full: Dict[str, Any] = response.json()
        results: List[Dict[str, Any]] = []
        # If no entities found
        if "entities" not in entity_dict_full:
            return results
        for qid, e in entity_dict_full["entities"].items():
            if qid not in entity_ids:
                logger.warning(
                    f"Wikidata redirect detected. " f"Returned entity id={qid} is not in list of entity ids."
                )
            if "missing" in e:
                logger.warning(f"Missing entity detected. Returned entity id={qid} is not in Wikidata found.")
                continue
            results.append(e)
        return results
