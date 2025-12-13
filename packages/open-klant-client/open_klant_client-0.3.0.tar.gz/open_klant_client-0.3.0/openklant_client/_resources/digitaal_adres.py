import uuid
from typing import cast

from ape_pie import APIClient

from openklant_client._resources.base import ResourceMixin
from openklant_client.types.pagination import PaginatedResponseBody
from openklant_client.types.resources.digitaal_adres import (
    DigitaalAdres,
    DigitaalAdresCreateData,
    ListDigitaalAdresParams,
)


class DigitaalAdresResource(ResourceMixin):
    http_client: APIClient
    base_path: str = "digitaleadressen"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.list_iter = self._make_list_iter(self.list)

    def list(
        self, *, params: ListDigitaalAdresParams | None = None
    ) -> PaginatedResponseBody[DigitaalAdres]:
        response = self._get(self.base_path, params=params)
        return cast(
            PaginatedResponseBody[DigitaalAdres], self.process_response(response)
        )

    def retrieve(self, /, uuid: str | uuid.UUID) -> DigitaalAdres:
        response = self._get(f"{self.base_path}/{str(uuid)}")
        return cast(DigitaalAdres, self.process_response(response))

    def create(
        self,
        *,
        data: DigitaalAdresCreateData,
    ) -> DigitaalAdres:
        response = self._post(self.base_path, data=data)
        return cast(DigitaalAdres, self.process_response(response))

    def delete(self, /, uuid: str):
        return self._delete(f"{self.base_path}/{str(uuid)}")
