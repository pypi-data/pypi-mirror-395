import pytest

from tests.validators import (
    MaakKlantContactCreateDataValidator,
    MaakKlantContactResponseValidator,
)


@pytest.mark.vcr
def test_create_klant_contact(client) -> None:
    data = MaakKlantContactCreateDataValidator.validate_python(
        {
            "klantcontact": {
                "kanaal": "contactformulier",
                "onderwerp": "vraag",
                "inhoud": "Dit is een vraag",
                "taal": "nld",
                "vertrouwelijk": True,
            },
            "betrokkene": {
                "rol": "klant",
                "initiator": True,
                "organisatienaam": "unknown",
            },
            "onderwerpobject": {
                "onderwerpobjectidentificator": {
                    "objectId": "OF-12345",
                    "codeObjecttype": "form",
                    "codeRegister": "openforms",
                    "codeSoortObjectId": "public_reference",
                }
            },
        }
    )
    resp = client.methods.maak_klant_contact(data=data)

    MaakKlantContactResponseValidator.validate_python(resp)
