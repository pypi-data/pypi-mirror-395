from typing import Literal, NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import Adres, ForeignKeyRef, FullForeigKeyRef

BetrokkeneRol = Literal["vertegenwoordiger", "klant"]


class CreateContactnaam(TypedDict):
    voorletters: NotRequired[str]
    voornaam: str
    voorvoegselAchternaam: NotRequired[str]
    achternaam: str


class BetrokkeneBaseCreateData(TypedDict):
    wasPartij: NotRequired[ForeignKeyRef | None]
    bezoekadres: NotRequired[Adres]
    correspondentieadres: NotRequired[Adres]
    contactnaam: NotRequired[CreateContactnaam | None]
    rol: BetrokkeneRol
    organisatienaam: str
    initiator: bool


class BetrokkeneCreateData(BetrokkeneBaseCreateData):
    hadKlantcontact: ForeignKeyRef


class Betrokkene(TypedDict):
    uuid: str
    url: str
    wasPartij: FullForeigKeyRef
    hadKlantcontact: FullForeigKeyRef
    digitaleAdressen: list[FullForeigKeyRef]
    bezoekadres: Adres
    correspondentieadres: Adres
    contactnaam: CreateContactnaam
    volledigeNaam: str
    rol: BetrokkeneRol
    organisatienaam: str
    initiator: bool


class BetrokkeneRetrieveParams(TypedDict):
    expand: NotRequired[list[Literal["digitaleAdressen",]]]
