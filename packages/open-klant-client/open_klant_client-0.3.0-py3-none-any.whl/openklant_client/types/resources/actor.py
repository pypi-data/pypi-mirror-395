from typing import Literal, NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import BooleanQueryParam

SoortActor = Literal["medewerker", "geautomatiseerde_actor", "organisatorische_eenheid"]


class ActorIdentificator(TypedDict):
    objectId: str
    codeObjecttype: str
    codeRegister: str
    codeSoortObjectId: str


class CreateActorData(TypedDict):
    naam: str
    soortActor: SoortActor
    indicatieActief: NotRequired[bool]
    actoridentificator: NotRequired[ActorIdentificator]


class Actor(TypedDict):
    uuid: str
    naam: str
    soortActor: SoortActor
    indicatieActief: bool
    actoridentificator: ActorIdentificator


class ActorListParams(TypedDict, total=False):
    actoridentificatorCodeObjecttype: str
    actoridentificatorCodeRegister: str
    actoridentificatorCodeSoortObjectId: str
    actoridentificatorObjectId: str
    indicatieActief: BooleanQueryParam
    naam: str
    page: int
    soortActor: SoortActor
