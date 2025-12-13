from typing import NotRequired

from typing_extensions import TypedDict

from openklant_client.types.common import ForeignKeyRef, FullForeigKeyRef


class OnderwerpObjectIdentificator(TypedDict):
    objectId: str
    codeObjecttype: str
    codeRegister: str
    codeSoortObjectId: str


class OnderwerpObjectBaseCreateData(TypedDict):
    wasKlantcontact: NotRequired[ForeignKeyRef | None]
    onderwerpobjectidentificator: NotRequired[OnderwerpObjectIdentificator | None]


class CreateOnderwerpObjectData(OnderwerpObjectBaseCreateData):
    klantcontact: NotRequired[ForeignKeyRef | None]


class OnderwerpObject(TypedDict):
    uuid: str
    url: str
    wasKlantcontact: FullForeigKeyRef | None
    klantcontact: FullForeigKeyRef | None
    onderwerpobjectidentificator: OnderwerpObjectIdentificator


class OnderwerpobjectIdentificatorListParams(TypedDict, total=False):
    onderwerpobjectidentificatorCodeObjecttype: str
    onderwerpobjectidentificatorCodeRegister: str
    onderwerpobjectidentificatorCodeSoortObjectId: str
    onderwerpobjectidentificatorObjectId: str
