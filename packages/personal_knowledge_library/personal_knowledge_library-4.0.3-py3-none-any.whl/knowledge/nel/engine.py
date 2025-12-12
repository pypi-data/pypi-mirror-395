# -*- coding: utf-8 -*-
# Copyright © 2021-present Wacom. All rights reserved.
from typing import Optional, List, Dict

from requests import Response

from knowledge.base.entity import LOCALE_TAG, TEXT_TAG
from knowledge.base.language import LocaleCode, EN_US
from knowledge.base.ontology import OntologyClassReference
from knowledge.nel.base import (
    PersonalEntityLinkingProcessor,
    EntitySource,
    KnowledgeSource,
    KnowledgeGraphEntity,
    EntityType,
)
from knowledge.services.base import handle_error, DEFAULT_MAX_RETRIES, DEFAULT_BACKOFF_FACTOR


class WacomEntityLinkingEngine(PersonalEntityLinkingProcessor):
    """
    Wacom Engine
    ------------
    Performing Wacom's Named entity linking.

    Parameter
    ---------
    service_url: str
        URL of the service
    service_endpoint: str
        Endpoint of the service
    """

    def __init__(
        self,
        service_url: str,
        application_name: str = "NEL Client",
        base_auth_url: Optional[str] = None,
        service_endpoint: str = "graph/v1",
        verify_calls: bool = True,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ):
        super().__init__(
            service_url=service_url,
            application_name=application_name,
            base_auth_url=base_auth_url,
            service_endpoint=service_endpoint,
            verify_calls=verify_calls,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

    def link_personal_entities(
        self, text: str, language_code: LocaleCode = EN_US, auth_key: Optional[str] = None, max_retries: int = 5
    ) -> List[KnowledgeGraphEntity]:
        """
        Performs Named Entity Linking on a text. It only finds entities which are accessible by the user identified by
        the auth key.

        Parameters
        ----------
        text: str
            Text where the entities shall be tagged in.
        language_code: LocaleCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        auth_key: Optional[str] (Default:= None)
            If the auth key is set, the logged-in user (if any) will be ignored and the auth key will be used.
        max_retries: int (Default:= 5)
            Maximum number of retries if the service is not available.

        Returns
        -------
        entities: List[KnowledgeGraphEntity]
            List of knowledge graph entities.

        Raises
        ------
        WacomServiceException
            If the Named Entity Linking service returns an error code.
        """
        named_entities: List[KnowledgeGraphEntity] = []
        url: str = f"{self.service_base_url}nel/text"

        payload: Dict[str, str] = {LOCALE_TAG: language_code, TEXT_TAG: text}
        # Define the retry policy

        response: Response = self.request_session.post(
            url, json=payload, verify=self.verify_calls, overwrite_auth_token=auth_key
        )
        if response.ok:
            results: dict = response.json()
            for e in results:
                entity_types: List[str] = []
                # --------------------------- Entity content -------------------------------------------------------
                source: Optional[EntitySource] = None
                if "uri" in e:
                    source = EntitySource(e["uri"], KnowledgeSource.WACOM_KNOWLEDGE)
                # --------------------------- Ontology types -------------------------------------------------------
                if "type" in e:
                    entity_types.append(e["type"])
                # --------------------------------------------------------------------------------------------------
                start: int = e["startPosition"]
                end: int = e["endPosition"]
                ne: KnowledgeGraphEntity = KnowledgeGraphEntity(
                    ref_text=text[start : end + 1],
                    start_idx=start,
                    end_idx=end,
                    label=e["value"],
                    confidence=0.0,
                    source=source,
                    content_link="",
                    ontology_types=entity_types,
                    entity_type=EntityType.PERSONAL_ENTITY,
                    tokens=e.get("tokens"),
                    token_indexes=e.get("tokenIndexes"),
                )
                ne.relevant_type = OntologyClassReference.parse(e["type"])
                named_entities.append(ne)
            return named_entities
        raise handle_error(f"Named entity linking for text:={text}@{language_code}. ", response)
