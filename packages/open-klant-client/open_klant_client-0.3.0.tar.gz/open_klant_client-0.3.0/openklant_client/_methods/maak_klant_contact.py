from typing import cast

from ape_pie import APIClient

from openklant_client._resources.base import ConvenienceMethodMixin
from openklant_client.types.methods.maak_klant_contact import (
    MaakKlantContactCreateData,
    MaakKlantContactResponse,
)


class MaakKlantContactConvenienceMethod(ConvenienceMethodMixin):
    """
    Convenience endpoint to create of KlantContact, Betrokkene and OnderwerpObject
    """

    http_client: APIClient
    base_path: str = "maak-klantcontact"

    def __call__(
        self,
        *,
        data: MaakKlantContactCreateData,
    ) -> MaakKlantContactResponse:
        response = self._post(self.base_path, data=data)
        return cast(MaakKlantContactResponse, self.process_response(response))
