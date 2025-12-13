from typing import NotRequired, TypedDict

from openklant_client.types.resources.betrokkene import (
    Betrokkene,
    BetrokkeneBaseCreateData,
)
from openklant_client.types.resources.klant_contact import (
    CreateKlantContactData,
    KlantContact,
)
from openklant_client.types.resources.onderwerp_object import (
    OnderwerpObject,
    OnderwerpObjectBaseCreateData,
)


class MaakKlantContactCreateData(TypedDict):
    klantcontact: CreateKlantContactData
    betrokkene: NotRequired[BetrokkeneBaseCreateData]
    onderwerpobject: NotRequired[OnderwerpObjectBaseCreateData]


class MaakKlantContactResponse(TypedDict):
    klantcontact: KlantContact
    betrokkene: Betrokkene | None
    onderwerpobject: OnderwerpObject | None
