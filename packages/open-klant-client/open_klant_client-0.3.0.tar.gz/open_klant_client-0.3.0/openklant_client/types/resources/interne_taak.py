from typing import Literal, NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import ForeignKeyRef, FullForeigKeyRef


class CreateInterneTaakData(TypedDict):
    nummer: NotRequired[str]
    gevraagdeHandeling: str
    aanleidinggevendKlantcontact: ForeignKeyRef
    toegewezenAanActor: ForeignKeyRef
    toelichting: NotRequired[str]
    status: Literal["te_verwerken", "verwerkt"]


class InterneTaak(TypedDict):
    uuid: str
    url: str
    nummer: str
    gevraagdeHandeling: str
    aanleidinggevendKlantcontact: FullForeigKeyRef
    toegewezenAanActor: FullForeigKeyRef
    toelichting: str
    status: Literal["te_verwerken", "verwerkt"]
    toegewezenOp: str
    afgehandeldOp: str | None
