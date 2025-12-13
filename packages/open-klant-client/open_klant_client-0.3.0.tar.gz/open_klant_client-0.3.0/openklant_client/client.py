from dataclasses import dataclass
from typing import Any

from ape_pie import APIClient
from ape_pie.typing import ConfigAdapter

from openklant_client._methods.maak_klant_contact import (
    MaakKlantContactConvenienceMethod,
)
from openklant_client._resources.actor import ActorResource
from openklant_client._resources.betrokkene import BetrokkeneResource
from openklant_client._resources.digitaal_adres import DigitaalAdresResource
from openklant_client._resources.interne_taak import InterneTaakResource
from openklant_client._resources.klant_contact import KlantContactResource
from openklant_client._resources.onderwerp_object import OnderwerpObjectResource
from openklant_client._resources.partij import PartijResource
from openklant_client._resources.partij_identificator import PartijIdentificatorResource


@dataclass
class ConvenienceMethods:
    """Container for non-resource centric, convenience method endpoints."""

    maak_klant_contact: MaakKlantContactConvenienceMethod


class OpenKlantClient(APIClient):
    partij: PartijResource
    partij_identificator: PartijIdentificatorResource
    digitaal_adres: DigitaalAdresResource
    klant_contact: KlantContactResource
    onderwerp_object: OnderwerpObjectResource
    actor: ActorResource
    interne_taak: InterneTaakResource
    betrokkene: BetrokkeneResource
    methods: ConvenienceMethods

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        request_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        if request_kwargs is None:
            request_kwargs = {}
        if "headers" not in request_kwargs:
            request_kwargs["headers"] = {}
        if token:
            request_kwargs["headers"]["Authorization"] = f"Token {token}"

        super().__init__(base_url=base_url, request_kwargs=request_kwargs)

        self.partij = PartijResource(self)
        self.partij_identificator = PartijIdentificatorResource(self)
        self.digitaal_adres = DigitaalAdresResource(self)
        self.klant_contact = KlantContactResource(self)
        self.onderwerp_object = OnderwerpObjectResource(self)
        self.actor = ActorResource(self)
        self.interne_taak = InterneTaakResource(self)
        self.betrokkene = BetrokkeneResource(self)
        self.methods = ConvenienceMethods(
            maak_klant_contact=MaakKlantContactConvenienceMethod(self)
        )

    @classmethod
    def configure_from(cls, adapter: ConfigAdapter, **kwargs):
        base_url = adapter.get_client_base_url()
        session_kwargs = adapter.get_client_session_kwargs()
        return cls(base_url, request_kwargs=session_kwargs, **kwargs)
