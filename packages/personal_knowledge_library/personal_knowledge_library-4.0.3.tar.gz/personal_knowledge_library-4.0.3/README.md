# Wacom Private Knowledge Library

[![Python package](https://github.com/Wacom-Developer/personal-knowledge-library/actions/workflows/python-package.yml/badge.svg)](https://github.com/Wacom-Developer/personal-knowledge-library/actions/workflows/python-package.yml)
[![Pylint](https://github.com/Wacom-Developer/personal-knowledge-library/actions/workflows/pylint.yml/badge.svg)](https://github.com/Wacom-Developer/personal-knowledge-library/actions/workflows/pylint.yml)

![License: Apache 2](https://img.shields.io/badge/License-Apache2-green.svg)
[![PyPI](https://img.shields.io/pypi/v/personal-knowledge-library.svg)](https://pypi.python.org/pypi/personal-knowledge-library)
[![PyPI](https://img.shields.io/pypi/pyversions/personal-knowledge-library.svg)](https://pypi.python.org/pypi/personal-knowledge-library)
[![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](https://developer-docs.wacom.com/docs/private-knowledge-service) 

![Contributors](https://img.shields.io/github/contributors/Wacom-Developer/personal-knowledge-library.svg)
![GitHub forks](https://img.shields.io/github/forks/Wacom-Developer/personal-knowledge-library.svg)
![GitHub stars](https://img.shields.io/github/stars/Wacom-Developer/personal-knowledge-library.svg)

The required tenant API key is only available for selected partner companies.
Please contact your Wacom representative for more information.

## Introduction

In knowledge management there is a distinction between data, information, and knowledge.
In the domain of digital ink this means:

- **Data—** The equivalent would be the ink strokes
- **Information—** After using handwriting-, shape-, math-, or other recognition processes, ink strokes are converted into machine-readable content, such as text, shapes, math representations, other digital content
- **Knowledge / Semantics** - Beyond recognition content needs to be semantically analyzed to become semantically understood based on shared common knowledge.

The following illustration shows the different layers of knowledge:
![Levels of ink knowledge layers](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/knowledge-levels.png)

For handling semantics, Wacom introduced the Wacom Private Knowledge (WPK) cloud service to manage personal ontologies and its associated personal knowledge graph.

This library provides simplified access to Wacom's personal knowledge cloud service.
It contains:

- Basic datastructures for an Ontology object and entities from the knowledge graph
- Clients for the REST APIs
- Connector for Wikidata public knowledge graph

**Ontology service:**

- List all Ontology structures
- Modify Ontology structures
- Delete Ontology structures

**Entity service:**

- List all entities
- Add entities to the knowledge graph
- Access object properties

**Search service:**

- Search for entities for labels and descriptions with a given language
- Search for literals (data properties) 
- Search for relations (object properties)

**Group service:**

- List all groups
- Add groups, modify groups, delete groups
- Add users and entities to groups

**Ontology service:**

- List all Ontology structures
- Modify Ontology structures

**Named Entity Linking service:**

- Linking words to knowledge entities from the graph in a given text (Ontology-based Named Entity Linking)

**Wikidata connector:**

- Import entities from Wikidata
- Mapping Wikidata entities to WPK entities

# Technology stack

## Domain Knowledge

The tasks of the ontology within Wacom's private knowledge system are to formalize the domain the technology is used in, such as education-, smart home-, or creative domain.
The domain model will be the foundation for the entities collected within the knowledge graph, describing real world concepts in a formal language understood by an artificial intelligence system:

- Foundation for structured data, knowledge representation as concepts and relations among concepts
- Being explicit definitions of shared vocabularies for interoperability
- Being actionable fragments of explicit knowledge that engines can use for inferencing (Reasoning)
- Can be used for problem-solving

An ontology defines (specifies) the concepts, relationships, and other distinctions that are relevant for modeling a domain.

## Knowledge Graph

- Knowledge graph is generated from unstructured and structured knowledge sources
- Contains all structured knowledge gathered from all sources
- Foundation for all semantic algorithms

## Semantic Technology

- Extract knowledge from various sources (Connectors)
- Linking words to knowledge entities from the graph in a given text (Ontology-based Named Entity Linking)
- Enables a smart search functionality which understands the context and finds related documents (Semantic Search)


# Functionality

## Import Format

For importing entities into the knowledge graph, the tools/import_entities.py script can be used.

The ThingObject supports a NDJSON-based import format, where the individual JSON files can contain the following structure.

| Field name             | Subfield name | Data Structure | Description                                                                                    |
|------------------------|---------------|----------------|------------------------------------------------------------------------------------------------|
| source_reference_id    |               | str            | A unique identifier for the entity used in the source system                                  |
| source_system          |               | str            | The source system describes the original source of the entity, such as wikidata, youtube, ... |
| image                  |               | str            | A string representing the URL of the entity's icon.                                           |
| labels                 |               | array          | An array of label objects, where each object has the following fields:                       |
|                        | value         | str            | A string representing the label text in the specified locale.                                |
|                        | locale        | str            | A string combining the ISO-3166 country code and the ISO-639 language code (e.g., "en-US").  |
|                        | isMain        | bool           | A boolean flag indicating if this label is the main label for the entity (true) or an alias (false). |
| descriptions           |               | array          | An array of description objects, where each object has the following fields:                 |
|                        | description   | str            | A string representing the description text in the specified locale.                          |
|                        | locale        | str            | A string combining the ISO-3166 country code and the ISO-639 language code (e.g., "en-US").  |
| type                   |               | str            | A string representing the IRI of the ontology class for this entity.                         |
| literals               |               | array[map]     | An array of data property objects, where each object has the following fields:               |


## Access API

The personal knowledge graph backend is implemented as a multi-tenancy system.
Thus, several tenants can be logically separated from each other and different organizations can build their one knowledge graph.

![Tenant concept](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/tenant-concept.png)

In general, a tenant with their users, groups, and entities are logically separated.
Physically, the entities are stored in the same instance of the Wacom Private Knowledge (WPK) backend database system.

The user management is rather limited, each organization must provide their own authentication service and user management.
The backend only has a reference of the user (*“shadow user”*) by an **external user id**.

The management of tenants is limited to the system owner —Wacom —, as it requires a **tenant management API** key.
While users for each tenant can be created by the owner of the **Tenant API Key**.
You will receive this token from the system owner after the creation of the tenant.


> :warning: Stores the **Tenant API Key** in a secure key store, as attackers can use the key to harm your system.


The **Tenant API Key** should be only used by your authentication service to create shadow users and to log in your user into the WPK backend.
After a successful user login, you will receive a token which can be used by the user to create, update, or delete entities and relations.

The following illustration summarizes the flows for creation of tenant and users:

![Tenant and user creation](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/tenant-user-creation.png)

The organization itself needs to implement their own authentication service which:

- handles the users and their passwords,
- controls the personal data of the users,
- connects the users with the WPK backend and share with them the user token.

The WPK backend only manages the access levels of the entities and the group management for users.
The illustration shows how the access token is received from the WPK endpoint:

![Access token request.](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/access-token.png)

# Entity API

The entities used within the knowledge graph and the relationship among them are defined within an ontology managed with Wacom Ontology Management System (WOMS).

An entity within the personal knowledge graphs consists of these major parts:

- **Icon—** a visual representation of the entity, for instance, a portrait of a person.
- **URI—** a unique resource identifier of an entity in the graph.
- **Type—** the type links to the defined concept class in the ontology.
- **Labels—** labels are the word(s) used in a language for the concept.
- **Description—** a short abstract that describes the entity.
- **Literals—** literals are properties of an entity, such as the first name of a person. The ontology defines all literals of the concept class as well as its data type.
- **Relations—** the relationship among different entities is described using relations.

The following illustration provides an example of an entity:

![Entity description](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/entity-description.png)

## Entity content

Entities in general are language-independent as across nationalities or cultures we only use different scripts and words for a shared instance of a concept.

Let's take Leonardo da Vinci as an example.
The ontology defines the concept of a Person, a human being.
Now, in English its label would be _Leonardo da Vinci_, while in Japanese _レオナルド・ダ・ヴィンチ_.
Moreover, he is also known as _Leonardo di ser Piero da Vinci_ or _ダ・ビンチ_.

### Labels

Now, in the given example all words that are assigned to the concept are labels.
The label _Leonardo da Vinci_ is stored in the backend with an additional language code, e.g. _en_.

There is always a main label, which refers to the most common or official name of an entity.
Another example would be Wacom, where _Wacom Co., Ltd._ is the official name while _Wacom_ is commonly used and be considered as an alias.

>  :pushpin: For the language code the **ISO 639-1:2002**, codes for the representation language names —Part 1: Alpha-2 code. Read more, [here](https://www.iso.org/standard/22109.html)

## Samples

### Entity handling

This samples shows how to work with the graph service.

```python
import argparse
from typing import Optional, Dict, List

from knowledge.base.entity import Description, Label
from knowledge.base.language import LocaleCode, EN_US, DE_DE
from knowledge.base.ontology import OntologyClassReference, OntologyPropertyReference, ThingObject, ObjectProperty
from knowledge.services.graph import WacomKnowledgeService

# ------------------------------- Knowledge entities -------------------------------------------------------------------
LEONARDO_DA_VINCI: str = 'Leonardo da Vinci'
SELF_PORTRAIT_STYLE: str = 'self-portrait'
ICON: str = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Mona_Lisa_%28copy%2C_Thalwil%2C_Switzerland%29."\
            "JPG/1024px-Mona_Lisa_%28copy%2C_Thalwil%2C_Switzerland%29.JPG"
# ------------------------------- Ontology class names -----------------------------------------------------------------
THING_OBJECT: OntologyClassReference = OntologyClassReference('wacom', 'core', 'Thing')
"""
The Ontology will contain a Thing class where is the root class in the hierarchy. 
"""
ARTWORK_CLASS: OntologyClassReference = OntologyClassReference('wacom', 'creative', 'VisualArtwork')
PERSON_CLASS: OntologyClassReference = OntologyClassReference('wacom', 'core', 'Person')
ART_STYLE_CLASS: OntologyClassReference = OntologyClassReference.parse('wacom:creative#ArtStyle')
IS_CREATOR: OntologyPropertyReference = OntologyPropertyReference('wacom', 'core', 'created')
HAS_TOPIC: OntologyPropertyReference = OntologyPropertyReference.parse('wacom:core#hasTopic')
CREATED: OntologyPropertyReference = OntologyPropertyReference.parse('wacom:core#created')
HAS_ART_STYLE: OntologyPropertyReference = OntologyPropertyReference.parse('wacom:creative#hasArtstyle')


def print_entity(display_entity: ThingObject, list_idx: int, client: WacomKnowledgeService,
                 short: bool = False):
    """
    Printing entity details.

    Parameters
    ----------
    display_entity: ThingObject
        Entity with properties
    list_idx: int
        Index with a list
    client: WacomKnowledgeService
        Knowledge graph client
    short: bool
        Short summary
    """
    print(f'[{list_idx}] : {display_entity.uri} <{display_entity.concept_type.iri}>')
    if len(display_entity.label) > 0:
        print('    | [Labels]')
        for la in display_entity.label:
            print(f'    |     |- "{la.content}"@{la.language_code}')
        print('    |')
    if not short:
        if len(display_entity.alias) > 0:
            print('    | [Alias]')
            for la in display_entity.alias:
                print(f'    |     |- "{la.content}"@{la.language_code}')
            print('    |')
        if len(display_entity.data_properties) > 0:
            print('    | [Attributes]')
            for data_property, labels in display_entity.data_properties.items():
                print(f'    |    |- {data_property.iri}:')
                for li in labels:
                    print(f'    |    |-- "{li.value}"@{li.language_code}')
            print('    |')

        relations_obj: Dict[OntologyPropertyReference, ObjectProperty] = client.relations(uri=display_entity.uri)
        if len(relations_obj) > 0:
            print('    | [Relations]')
            for r_idx, re in enumerate(relations_obj.values()):
                last: bool = r_idx == len(relations_obj) - 1
                print(f'    |--- {re.relation.iri}: ')
                print(f'    {"|" if not last else " "}       |- [Incoming]: {re.incoming_relations} ')
                print(f'    {"|" if not last else " "}       |- [Outgoing]: {re.outgoing_relations}')
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default='https://private-knowledge.wacom.com',
                        help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom personal knowledge REST API Client
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(service_url=args.instance, application_name="Wacom Knowledge Listing")
    knowledge_client.login(args.tenant, args.user)
    page_id: Optional[str] = None
    page_number: int = 1
    entity_count: int = 0
    print('-----------------------------------------------------------------------------------------------------------')
    print(' First step: Find Leonardo da Vinci in the knowledge graph.')
    print('-----------------------------------------------------------------------------------------------------------')
    res_entities, next_search_page = knowledge_client.search_labels(search_term=LEONARDO_DA_VINCI,
                                                                    language_code=LocaleCode('en_US'), limit=1000)
    leo: Optional[ThingObject] = None
    s_idx: int = 1
    for res_entity in res_entities:
        #  Entity must be a person and the label matches with full string
        if res_entity.concept_type == PERSON_CLASS and LEONARDO_DA_VINCI in [la.content for la in res_entity.label]:
            leo = res_entity
            break

    print('-----------------------------------------------------------------------------------------------------------')
    print(' What artwork exists in the knowledge graph.')
    print('-----------------------------------------------------------------------------------------------------------')
    relations_dict: Dict[OntologyPropertyReference, ObjectProperty] = knowledge_client.relations(uri=leo.uri)
    print(f' Artwork of {leo.label}')
    print('-----------------------------------------------------------------------------------------------------------')
    idx: int = 1
    if CREATED in relations_dict:
        for e in relations_dict[CREATED].outgoing_relations:
            print(f' [{idx}] {e.uri}: {e.label}')
            idx += 1
    print('-----------------------------------------------------------------------------------------------------------')
    print(' Let us create a new piece of artwork.')
    print('-----------------------------------------------------------------------------------------------------------')

    # Main labels for entity
    artwork_labels: List[Label] = [
        Label('Ginevra Gherardini', EN_US),
        Label('Ginevra Gherardini', DE_DE)
    ]
    # Alias labels for entity
    artwork_alias: List[Label] = [
        Label("Ginevra", EN_US),
        Label("Ginevra", DE_DE)
    ]
    # Topic description
    artwork_description: List[Description] = [
        Description('Oil painting of Mona Lisa\' sister', EN_US),
        Description('Ölgemälde von Mona Lisa\' Schwester', DE_DE)
    ]
    # Topic
    artwork_object: ThingObject = ThingObject(label=artwork_labels, concept_type=ARTWORK_CLASS,
                                              description=artwork_description,
                                              icon=ICON)
    artwork_object.alias = artwork_alias
    print(f' Create: {artwork_object}')
    # Create artwork
    artwork_entity_uri: str = knowledge_client.create_entity(artwork_object)
    print(f' Entity URI: {artwork_entity_uri}')
    # Create relation between Leonardo da Vinci and artwork
    knowledge_client.create_relation(source=leo.uri, relation=IS_CREATOR, target=artwork_entity_uri)

    relations_dict = knowledge_client.relations(uri=artwork_entity_uri)
    for ontology_property, object_property in relations_dict.items():
        print(f'  {object_property}')
    # You will see that wacom:core#isCreatedBy is automatically inferred as a relation as it is the inverse property of
    # wacom:core#created.

    # Now, more search options
    res_entities, next_search_page = knowledge_client.search_description('Michelangelo\'s Sistine Chapel',
                                                                         EN_US, limit=1000)
    print('-----------------------------------------------------------------------------------------------------------')
    print(' Search results.  Description: "Michelangelo\'s Sistine Chapel"')
    print('-----------------------------------------------------------------------------------------------------------')
    s_idx: int = 1
    for e in res_entities:
        print_entity(e, s_idx, knowledge_client)

    # Now, let's search all artwork that has the art style self-portrait
    res_entities, next_search_page = knowledge_client.search_labels(search_term=SELF_PORTRAIT_STYLE,
                                                                    language_code=EN_US, limit=1000)
    art_style: Optional[ThingObject] = None
    s_idx: int = 1
    for entity in res_entities:
        #  Entity must be a person and the label matches with full string
        if entity.concept_type == ART_STYLE_CLASS and SELF_PORTRAIT_STYLE in [la.content for la in entity.label]:
            art_style = entity
            break
    res_entities, next_search_page = knowledge_client.search_relation(subject_uri=None,
                                                                      relation=HAS_ART_STYLE,
                                                                      object_uri=art_style.uri,
                                                                      language_code=EN_US)
    print('-----------------------------------------------------------------------------------------------------------')
    print(' Search results.  Relation: relation:=has_topic  object_uri:= unknown')
    print('-----------------------------------------------------------------------------------------------------------')
    s_idx: int = 1
    for e in res_entities:
        print_entity(e, s_idx, knowledge_client, short=True)
        s_idx += 1

    # Finally, the activation function retrieving the related identities to a pre-defined depth.
    entities, relations = knowledge_client.activations(uris=[leo.uri], depth=1)
    print('-----------------------------------------------------------------------------------------------------------')
    print(f'Activation.  URI: {leo.uri}')
    print('-----------------------------------------------------------------------------------------------------------')
    s_idx: int = 1
    for e in res_entities:
        print_entity(e, s_idx, knowledge_client)
        s_idx += 1
    # All relations
    print('-----------------------------------------------------------------------------------------------------------')
    for r in relations:
        print(f'Subject: {r[0]} Predicate: {r[1]} Object: {r[2]}')
    print('-----------------------------------------------------------------------------------------------------------')
    page_id = None

    # Listing all entities that have the type
    idx: int = 1
    while True:
        # pull
        entities, total_number, next_page_id = knowledge_client.listing(ART_STYLE_CLASS, page_id=page_id, limit=100)
        pulled_entities: int = len(entities)
        entity_count += pulled_entities
        print('-------------------------------------------------------------------------------------------------------')
        print(f' Page: {page_number} Number of entities: {len(entities)}  ({entity_count}/{total_number}) '
              f'Next page id: {next_page_id}')
        print('-------------------------------------------------------------------------------------------------------')
        for e in entities:
            print_entity(e, idx, knowledge_client)
            idx += 1
        if pulled_entities == 0:
            break
        page_number += 1
        page_id = next_page_id
    print()
    # Delete all personal entities for this user
    while True:
        # pull
        entities, total_number, next_page_id = knowledge_client.listing(THING_OBJECT, page_id=page_id,
                                                                        limit=100)
        pulled_entities: int = len(entities)
        if pulled_entities == 0:
            break
        delete_uris: List[str] = [e.uri for e in entities]
        print(f'Cleanup. Delete entities: {delete_uris}')
        knowledge_client.delete_entities(uris=delete_uris, force=True)
        page_number += 1
        page_id = next_page_id
    print('-----------------------------------------------------------------------------------------------------------')
```

### Named Entity Linking 

Performing Named Entity Linking (NEL) on text and Universal Ink Model.

```python
import argparse
from typing import List, Dict

import urllib3

from knowledge.base.language import EN_US
from knowledge.base.ontology import OntologyPropertyReference, ThingObject, ObjectProperty
from knowledge.nel.base import KnowledgeGraphEntity
from knowledge.nel.engine import WacomEntityLinkingEngine
from knowledge.services.graph import WacomKnowledgeService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


TEXT: str = "Leonardo da Vinci painted the Mona Lisa."


def print_entity(entity: KnowledgeGraphEntity, list_idx: int, auth_key: str, client: WacomKnowledgeService):
    """
    Printing entity details.

    Parameters
    ----------
    entity: KnowledgeGraphEntity
        Named entity
    list_idx: int
        Index with a list
    auth_key: str
        Authorization key
    client: WacomKnowledgeService
        Knowledge graph client
    """
    thing: ThingObject = knowledge_client.entity(auth_key=user_token, uri=entity.entity_source.uri)
    print(f'[{list_idx}] - {entity.ref_text} [{entity.start_idx}-{entity.end_idx}] : {thing.uri}'
          f' <{thing.concept_type.iri}>')
    if len(thing.label) > 0:
        print('    | [Labels]')
        for la in thing.label:
            print(f'    |     |- "{la.content}"@{la.language_code}')
        print('    |')
    if len(thing.label) > 0:
        print('    | [Alias]')
        for la in thing.alias:
            print(f'    |     |- "{la.content}"@{la.language_code}')
        print('    |')
    relations: Dict[OntologyPropertyReference, ObjectProperty] = client.relations(auth_key=auth_key, uri=thing.uri)
    if len(thing.data_properties) > 0:
        print('    | [Attributes]')
        for data_property, labels in thing.data_properties.items():
            print(f'    |    |- {data_property.iri}:')
            for li in labels:
                print(f'    |    |-- "{li.value}"@{li.language_code}')
        print('    |')
    if len(relations) > 0:
        print('    | [Relations]')
        for re in relations.values():
            print(f'    |--- {re.relation.iri}: ')
            print(f'           |- [Incoming]: {re.incoming_relations} ')
            print(f'           |- [Outgoing]: {re.outgoing_relations}')
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default="https://private-knowledge.wacom.com", help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom personal knowledge REST API Client
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(
        application_name="Named Entity Linking Knowledge access",
        service_url=args.instance)
    #  Wacom Named Entity Linking
    nel_client: WacomEntityLinkingEngine = WacomEntityLinkingEngine(
        service_url=args.instance,
        service_endpoint=WacomEntityLinkingEngine.SERVICE_ENDPOINT
    )
    # Use special tenant for testing: Unit-test tenant
    user_token, refresh_token, expiration_time = nel_client.request_user_token(TENANT_KEY, EXTERNAL_USER_ID)
    entities: List[KnowledgeGraphEntity] = nel_client.\
        link_personal_entities(text=TEXT, language_code=EN_US, auth_key=user_token)
    idx: int = 1
    print('-----------------------------------------------------------------------------------------------------------')
    print(f'Text: "{TEXT}"@{EN_US}')
    print('-----------------------------------------------------------------------------------------------------------')
    for e in entities:
        print_entity(e, idx, user_token, knowledge_client)
        idx += 1

```

### Access Management

The sample shows how access to entities can be shared with a group of users or the tenant.

```python
import argparse
from typing import List

from knowledge.base.entity import Label, Description
from knowledge.base.language import EN_US, DE_DE, JA_JP
from knowledge.base.ontology import OntologyClassReference, ThingObject
from knowledge.services.base import WacomServiceException
from knowledge.services.graph import WacomKnowledgeService
from knowledge.services.group import GroupManagementService, Group
from knowledge.services.users import UserManagementServiceAPI

# ------------------------------- User credential ----------------------------------------------------------------------
TOPIC_CLASS: OntologyClassReference = OntologyClassReference('wacom', 'core', 'Topic')


def create_entity() -> ThingObject:
    """Create a new entity.

    Returns
    -------
    entity: ThingObject
        Entity object
    """
    # Main labels for entity
    topic_labels: List[Label] = [
        Label('Hidden', EN_US),
        Label('Versteckt', DE_DE),
        Label('隠れた', JA_JP),
    ]

    # Topic description
    topic_description: List[Description] = [
        Description('Hidden entity to explain access management.', EN_US),
        Description('Verstecke Entität, um die Zugriffsteuerung zu erklären.', DE_DE)
    ]
    # Topic
    topic_object: ThingObject = ThingObject(label=topic_labels, concept_type=TOPIC_CLASS, description=topic_description)
    return topic_object


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default='https://private-knowledge.wacom.com',
                        help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom personal knowledge REST API Client
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(application_name="Wacom Knowledge Listing",
                                                                    service_url=args.instance)
    # User Management
    user_management: UserManagementServiceAPI = UserManagementServiceAPI(service_url=args.instance)
    # Group Management
    group_management: GroupManagementService = GroupManagementService(service_url=args.instance)
    admin_token, refresh_token, expiration_time = user_management.request_user_token(TENANT_KEY, EXTERNAL_USER_ID)
    # Now, we create a user
    u1, u1_token, _, _ = user_management.create_user(TENANT_KEY, "u1")
    u2, u2_token, _, _ = user_management.create_user(TENANT_KEY, "u2")
    u3, u3_token, _, _ = user_management.create_user(TENANT_KEY, "u3")

    # Now, let's create an entity
    thing: ThingObject = create_entity()
    entity_uri: str = knowledge_client.create_entity(thing, auth_key=u1_token)
    # Only user 1 can access the entity from cloud storage
    my_thing: ThingObject = knowledge_client.entity(entity_uri, auth_key=u1_token)
    print(f'User is the owner of {my_thing.owner}')
    # Now only user 1 has access to the personal entity
    knowledge_client.entity(entity_uri, auth_key=u1_token)
    # Try to access the entity
    try:
        knowledge_client.entity(entity_uri, auth_key=u2_token)
    except WacomServiceException as we:
        print(f"Expected exception as user 2 has no access to the personal entity of user 1. Exception: {we}")
        print(f"Status code: {we.status_code}")
        print(f"Response text: {we.service_response}")
    # Try to access the entity
    try:
        knowledge_client.entity(entity_uri, auth_key=u3_token)
    except WacomServiceException as we:
        print(f"Expected exception as user 3 has no access to the personal entity of user 1. Exception: {we}")
    # Now, user 1 creates a group
    g: Group = group_management.create_group("test-group", auth_key=u1_token)
    # Shares the join key with user 2 and user 2 joins
    group_management.join_group(g.id, g.join_key, auth_key=u2_token)
    # Share entity with a group
    group_management.add_entity_to_group(g.id, entity_uri, auth_key=u1_token)
    # Now, user 2 should have access
    other_thing: ThingObject = knowledge_client.entity(entity_uri, auth_key=u2_token)
    print(f'User 2 is the owner of the thing: {other_thing.owner}')
    # Try to access the entity
    try:
        knowledge_client.entity(entity_uri, auth_key=u3_token)
    except WacomServiceException as we:
        print(f"Expected exception as user 3 still has no access to the personal entity of user 1. Exception: {we}")
        print(f"URL: {we.url}, method: {we.method}")
        print(f"Status code: {we.status_code}")
        print(f"Response text: {we.service_response}")
        print(f"Message: {we.message}")
    # Un-share the entity
    group_management.remove_entity_to_group(g.id, entity_uri, auth_key=u1_token)
    # Now, again no access
    try:
        knowledge_client.entity(entity_uri, auth_key=u2_token)
    except WacomServiceException as we:
        print(f"Expected exception as user 2 has no access to the personal entity of user 1. Exception: {we}")
        print(f"URL: {we.url}, method: {we.method}")
        print(f"Status code: {we.status_code}")
        print(f"Response text: {we.service_response}")
        print(f"Message: {we.message}")
    group_management.leave_group(group_id=g.id, auth_key=u2_token)
    # Now, share the entity with the whole tenant
    my_thing.tenant_access_right.read = True
    knowledge_client.update_entity(my_thing, auth_key=u1_token)
    # Now, all users can access the entity
    knowledge_client.entity(entity_uri, auth_key=u2_token)
    knowledge_client.entity(entity_uri, auth_key=u3_token)
    # Finally, clean up
    knowledge_client.delete_entity(entity_uri, force=True, auth_key=u1_token)
    # Remove users
    user_management.delete_user(TENANT_KEY, u1.external_user_id, u1.id, force=True)
    user_management.delete_user(TENANT_KEY, u2.external_user_id, u2.id, force=True)
    user_management.delete_user(TENANT_KEY, u3.external_user_id, u3.id, force=True)

```

### Ontology Creation

The samples show how the ontology can be extended and new entities can be added using the added classes.

```python
import argparse
import sys
from typing import Optional, List

from knowledge.base.entity import Label, Description
from knowledge.base.language import EN_US, DE_DE
from knowledge.base.ontology import DataPropertyType, OntologyClassReference, OntologyPropertyReference, ThingObject, \
    DataProperty, OntologyContext
from knowledge.services.graph import WacomKnowledgeService
from knowledge.services.ontology import OntologyService
from knowledge.services.session import PermanentSession

# ------------------------------- Constants ----------------------------------------------------------------------------
LEONARDO_DA_VINCI: str = 'Leonardo da Vinci'
CONTEXT_NAME: str = 'core'
# Wacom Base Ontology Types
PERSON_TYPE: OntologyClassReference = OntologyClassReference.parse("wacom:core#Person")
# Demo Class
ARTIST_TYPE: OntologyClassReference = OntologyClassReference.parse("demo:creative#Artist")
# Demo Object property
IS_INSPIRED_BY: OntologyPropertyReference = OntologyPropertyReference.parse("demo:creative#isInspiredBy")
# Demo Data property
STAGE_NAME: OntologyPropertyReference = OntologyPropertyReference.parse("demo:creative#stageName")


def create_artist() -> ThingObject:
    """
    Create a new artist entity.
    Returns
    -------
    instance: ThingObject
        Artist entity
    """
    # Main labels for entity
    topic_labels: List[Label] = [
        Label('Gian Giacomo Caprotti', EN_US),
    ]

    # Topic description
    topic_description: List[Description] = [
        Description('Hidden entity to explain access management.', EN_US),
        Description('Verstecke Entität, um die Zugriffsteuerung zu erlären.', DE_DE)
    ]

    data_property: DataProperty = DataProperty(content='Salaj',
                                               property_ref=STAGE_NAME,
                                               language_code=EN_US)
    # Topic
    artist: ThingObject = ThingObject(label=topic_labels, concept_type=ARTIST_TYPE, description=topic_description)
    artist.add_data_property(data_property)
    return artist


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default="https://private-knowledge.wacom.com", help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom Ontology REST API Client
    ontology_client: OntologyService = OntologyService(service_url=args.instance)
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(
        application_name="Ontology Creation Demo",
        service_url=args.instance)
    # Login as admin user
    session: PermanentSession = ontology_client.login(TENANT_KEY, EXTERNAL_USER_ID)
    if session.roles != "TenantAdmin":
        print(f'User {EXTERNAL_USER_ID} is not an admin user.')
        sys.exit(1)
    knowledge_client.use_session(session.id)
    knowledge_client.ontology_update()
    context: Optional[OntologyContext] = ontology_client.context()
    if context is None:
        # First, create a context for the ontology
        ontology_client.create_context(name=CONTEXT_NAME, base_uri=f'demo:{CONTEXT_NAME}')
        context_name: str = CONTEXT_NAME
    else:
        context_name: str = context.context
    # Creating a class which is a subclass of a person
    ontology_client.create_concept(context_name, reference=ARTIST_TYPE, subclass_of=PERSON_TYPE)

    # Object properties
    ontology_client.create_object_property(context=context_name, reference=IS_INSPIRED_BY, domains_cls=[ARTIST_TYPE],
                                           ranges_cls=[PERSON_TYPE], inverse_of=None, subproperty_of=None)
    # Data properties
    ontology_client.create_data_property(context=context_name, reference=STAGE_NAME,
                                         domains_cls=[ARTIST_TYPE],
                                         ranges_cls=[DataPropertyType.STRING],
                                         subproperty_of=None)
    # Commit the changes of the ontology. This is very important to confirm changes.
    ontology_client.commit(context=context_name)
    # Trigger graph service. After the update the ontology is available and the new entities can be created
    knowledge_client.ontology_update()

    res_entities, next_search_page = knowledge_client.search_labels(search_term=LEONARDO_DA_VINCI,
                                                                    language_code=EN_US, limit=1000)
    leo: Optional[ThingObject] = None
    for entity in res_entities:
        #  Entity must be a person and the label matches with full string
        if entity.concept_type == PERSON_TYPE and LEONARDO_DA_VINCI in [la.content for la in entity.label]:
            leo = entity
            break

    artist_student: ThingObject = create_artist()
    artist_student_uri: str = knowledge_client.create_entity(artist_student)
    knowledge_client.create_relation(artist_student_uri, IS_INSPIRED_BY, leo.uri)

```

### Asynchronous Client 

The sample shows how to use the asynchronous client. 
Most of the methods are available in the asynchronous client(s).
Only for the ontology management the asynchronous client is not available.

```python
import argparse
import asyncio
import uuid
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

from knowledge.base.entity import Label
from knowledge.base.language import LanguageCode, EN, SUPPORTED_LOCALES, EN_US
from knowledge.base.ontology import ThingObject
from knowledge.ontomapping import load_configuration
from knowledge.ontomapping.manager import wikidata_to_thing
from knowledge.public.relations import wikidata_relations_extractor
from knowledge.public.wikidata import WikidataSearchResult, WikidataThing
from knowledge.public.client import WikiDataAPIClient
from knowledge.services.asyncio.graph import AsyncWacomKnowledgeService
from knowledge.services.asyncio.group import AsyncGroupManagementService
from knowledge.services.asyncio.users import AsyncUserManagementService
from knowledge.services.base import WacomServiceException, format_exception
from knowledge.services.group import Group
from knowledge.services.session import PermanentSession, RefreshableSession
from knowledge.services.users import UserRole, User


def import_entity_from_wikidata(search_term: str, locale: LanguageCode) -> Dict[str, ThingObject]:
    """
    Import entity from Wikidata.
    Parameters
    ----------
    search_term: str
        Search term
    locale: LanguageCode
        Language code

    Returns
    -------
    things: Dict[str, ThingObject]
        Mapping qid to a thing object
    """
    search_results: List[WikidataSearchResult] = WikiDataAPIClient.search_term(search_term, locale)
    # Load mapping configuration
    load_configuration(Path(__file__).parent.parent / 'pkl-cache' / 'ontology_mapping.json')
    # Search wikidata for entities
    qid_entities: List[WikidataThing] = WikiDataAPIClient.retrieve_entities([sr.qid for sr in search_results])
    qid_things: Dict[str, WikidataThing] = {qt.qid: qt for qt in qid_entities}
    relations: Dict[str, List[Dict[str, Any]]] = wikidata_relations_extractor(qid_things)
    # Now, let's create the things
    things: Dict[str, ThingObject] = {}
    for res in qid_entities:
        wikidata_thing, import_warnings = wikidata_to_thing(res, all_relations=relations,
                                                            supported_locales=SUPPORTED_LOCALES,
                                                            pull_wikipedia=True,
                                                            all_wikidata_objects=qid_things)
        things[res.qid] = wikidata_thing
    return things


async def user_management_sample(tenant_api_key: str, instance: str) -> Tuple[User, str, str]:
    """
    User management sample.
    Parameters
    ----------
    tenant_api_key: str
        Session
    instance: str
        Instance URL

    Returns
    -------
    user: User
        User object
    user_token: str
        User token
    refresh_token: str
        Refresh token
    """
    user_management: AsyncUserManagementService = AsyncUserManagementService(
                                                    application_name="Async user management sample",
                                                    service_url=instance)
    meta_data: dict = {'user-type': 'demo'}
    user, user_token, refresh_token, _ = await user_management.create_user(tenant_key=tenant_api_key,
                                                                           external_id=uuid.uuid4().hex,
                                                                           meta_data=meta_data,
                                                                           roles=[UserRole.USER])
    return user, user_token, refresh_token


async def clean_up(instance: str, tenant_api_key: str):
    """
    Cleanup sample.
    Parameters
    ----------
    instance: str
        Instance URL
    tenant_api_key: str
        Tenant API key
    """
    user_management: AsyncUserManagementService = AsyncUserManagementService(
                                                    application_name="Async user management sample",
                                                    service_url=instance)
    users: List[User] = await user_management.listing_users(tenant_api_key)
    for user in users:
        if 'user-type' in user.meta_data and user.meta_data['user-type'] == 'demo':
            await user_management.delete_user(tenant_key=tenant_api_key, external_id=user.external_user_id,
                                              internal_id=user.id, force=True)


async def main(external_user_id: str, tenant_api_key: str, instance: str):
    """
    Main function for the async sample.

    Parameters
    ----------
    external_user_id: str
        External id of the shadow user within the Wacom Personal Knowledge.
    tenant_api_key: str
        Tenant api key of the shadow user within the Wacom Personal Knowledge.
    instance: str
        URL of instance
    """
    async_client: AsyncWacomKnowledgeService = AsyncWacomKnowledgeService(application_name="Async sample",
                                                                          service_url=instance)
    permanent_session: PermanentSession = await async_client.login(tenant_api_key=tenant_api_key,
                                                                   external_user_id=external_user_id)
    """
    The permanent session contains the external user id, the tenant id, thus it is capable to refresh the token and 
    re-login if needed. The functions check if the token is expired and refresh it if needed. Internally, the token 
    manager handles the session. There are three different session types:
    - Permanent session: The session is refreshed automatically if needed.
    - Refreshable session: The session is not refreshed automatically using the refresh token, 
                           but if the session is not used for a day the refresh token is invalidated.
    - Timed session: The session is only has the authentication token and no refresh token. Thus, it times out after
                     one hour.
    """
    print(f'Service instance: {async_client.service_url}')
    print('-' * 100)
    print(f'Logged in as {permanent_session.external_user_id} (tenant id: {permanent_session.tenant_id}) ')
    is_ten_admin: bool = permanent_session.roles == "TenantAdmin"
    print(f'Is tenant admin: {is_ten_admin}')
    print('-' * 100)
    print(f'Token information')
    print('-' * 100)
    print(f'Refreshable: {permanent_session.refreshable}')
    print(f'Token must be refreshed before: {permanent_session.expiration} UTC')
    print(f'Token expires in {permanent_session.expires_in} seconds)')
    print('-' * 100)
    print(f'Creating two users')
    print('-' * 100)
    # User management sample
    user_1, user_token_1, refresh_token_1 = await user_management_sample(tenant_api_key, instance)
    print(f'User: {user_1}')
    user_2, user_token_2, refresh_token_2 = await user_management_sample(tenant_api_key, instance)
    print(f'User: {user_2}')
    print('-' * 100)
    async_client_user_1: AsyncWacomKnowledgeService = AsyncWacomKnowledgeService(application_name="Async user 1",
                                                                                 service_url=instance)
    refresh_session_1: RefreshableSession = await async_client_user_1.register_token(auth_key=user_token_1,
                                                                                     refresh_token=refresh_token_1)
    async_client_user_2: AsyncWacomKnowledgeService = AsyncWacomKnowledgeService(application_name="Async sample",
                                                                                 service_url=instance)
    await async_client_user_2.register_token(auth_key=user_token_2, refresh_token=refresh_token_2)
    """
    Now, let's create some entities.
    """
    print('Creation of entities')
    print('-' * 100)
    things_objects: Dict[str, ThingObject] = import_entity_from_wikidata('Leonardo da Vinci', EN)
    created: List[ThingObject] = await async_client_user_1.create_entity_bulk(list(things_objects.values()))
    for thing in created:
        try:
            await async_client_user_2.entity(thing.uri)
        except WacomServiceException as we:
            print(f'User 2 cannot see entity {thing.uri}.\n{format_exception(we)}')

    # Now using the group management service
    group_management: AsyncGroupManagementService = AsyncGroupManagementService(application_name="Group management",
                                                                                service_url=instance)
    await group_management.use_session(refresh_session_1.id)
    # User 1 creates a group
    new_group: Group = await group_management.create_group("sample-group")
    for thing in created:
        try:
            await group_management.add_entity_to_group(new_group.id, thing.uri)
        except WacomServiceException as we:
            print(f'User 1 cannot delete entity {thing.uri}.\n{format_exception(we)}')
    await group_management.add_user_to_group(new_group.id, user_2.id)
    print(f'User 2 can see the entities now. Let us check with async client 2. '
          f'Id of the user: {async_client_user_2.current_session.external_user_id}')
    for thing in created:
        iter_thing: ThingObject = await async_client_user_2.entity(thing.uri)
        label: Optional[Label] = iter_thing.label_lang(EN_US)
        print(f'User 2 can see entity {label.content if label else "UNKNOWN"} {iter_thing.uri}.'
              f'Ownership: owner flag:={iter_thing.owner}, owner is {iter_thing.owner_id}.')
    print('-' * 100)
    await clean_up(instance=instance, tenant_api_key=tenant_api_key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default='https://private-knowledge.wacom.com',
                        help="URL of instance")
    args = parser.parse_args()
    asyncio.run(main(args.user, args.tenant, args.instance))
```
### Semantic Search

The sample shows how to use the semantic search.
There are two types of search:
- Label search
- Document search

The label search is used to find entities based on the label.
The document search is used to find documents based on the content.


```python
import argparse
import re
import time
from typing import List, Dict, Any

from knowledge.base.language import EN_US
from knowledge.base.search import LabelMatchingResponse, DocumentSearchResponse, VectorDBDocument
from knowledge.services.search import SemanticSearchClient


def clean_text(text: str, max_length: int = -1) -> str:
    """
    Clean text from new lines and multiple spaces.

    Parameters
    ----------
    text: str
        Text to clean.
    max_length: int [default=-1]
        Maximum length of the cleaned text. If the length is-1, then the text is not truncated.

    Returns
    -------
    str
        Cleaned text.
    """
    # First, remove new lines
    text = text.strip().replace('\n', ' ')
    # Then remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    if 0 < max_length < len(text):
        return text[:max_length] + '...'
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Personal Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default="https://private-knowledge.wacom.com", help="URL of instance")
    args = parser.parse_args()
    client: SemanticSearchClient = SemanticSearchClient(service_url=args.instance)
    session = client.login(args.tenant, args.user)
    max_results: int = 10
    labels_count: int = client.count_documents(locale=EN_US)
    print(f"Tenant ID: {client.current_session.tenant_id} | Labels count: {labels_count} for [locale:={EN_US}]")
    t0: float = time.time()
    results: LabelMatchingResponse = client.labels_search(query="Leonardo Da Vinci", locale=EN_US,
                                                          max_results=max_results)
    t1: float = time.time()
    if len(results.results) > 0:
        print("=" * 120)
        for idx, res in enumerate(results.results):
            print(f"{idx + 1}. {res.label} | Relevance: ({res.score:.2f}) | URI: {res.entity_uri}")
        all_labels: List[VectorDBDocument] = client.retrieve_labels(EN_US, results.results[0].entity_uri)
        print("=" * 120)
        print(f"Labels for best match: {results.results[0].entity_uri}")
        for idx, label in enumerate(all_labels):
            print(f"{idx + 1}. {label.content}")
    print("=" * 120)
    print(f"Time: {(t1 - t0) * 1000:.2f} ms")
    print("=" * 120)
    document_count: int = client.count_documents(locale=EN_US)
    print(f"Document count: {document_count} for [locale:={EN_US}]")
    t2: float = time.time()
    document_results: DocumentSearchResponse = client.document_search(query="Leonardo Da Vinci artwork", locale=EN_US,
                                                                      max_results=max_results)
    t3: float = time.time()
    print("=" * 120)
    if len(document_results.results) > 0:

        for idx, res in enumerate(document_results.results):
            print(f"{idx + 1}.  URI: {res.content_uri} | Relevance: {res.score:.2f} | Chunk:"
                  f"\n\t{clean_text(res.content_chunk, max_length=100)}")
        print(f"\n All document chunks for best match: {document_results.results[0].content_uri}")
        print("=" * 120)
        # If you need all document chunks, you can retrieve them using the content_uri.
        best_match_uri: str = document_results.results[0].content_uri
        chunks: List[VectorDBDocument] = client.retrieve_documents_chunks(locale=EN_US, uri=best_match_uri)
        metadata: Dict[str, Any] = document_results.results[0].metadata
        for idx, chunk in enumerate(chunks):
            print(f"{idx + 1}. {clean_text(chunk.content)}")
        print("\n\tMetadata:\n\t---------")
        for key, value in metadata.items():
            print(f"\t- {key}: {clean_text(value, max_length=100) if isinstance(value, str) else value }")
    print("=" * 120)
    print(f"Time: {(t3 - t2) * 1000:.2f} ms")
    print("=" * 120)
```

# Documentation

You can find more detailed technical documentation, [here](https://developer-docs.wacom.com/preview/semantic-ink/).
API documentation is available [here](./docs/).

## Contributing
Contribution guidelines are still a work in progress.

## License
[Apache License 2.0](LICENSE)
