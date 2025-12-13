=================
Open Klant Client
=================

A Python client library for interacting with the `Open Klant API <https://github.com/maykinmedia/open-klant>`_.

Installation
============

.. code-block:: bash

    pip install open-klant-client

Usage
=====

Initialize the client with your API endpoint and token:

.. code-block:: python

    from openklant_client import OpenKlantClient

    client = OpenKlantClient(
        base_url="https://example.com/klantinteracties/api/v1",
        token="your_api_token"
    )

List resources
--------------

.. code-block:: python

    # List all partijen
    partijen = client.partij.list()

    # List klantcontacten with filters
    contacten = client.klant_contact.list(params={"onderwerp": "vraag"})

    # Auto-paginate through all results (max_requests=None means paginate until all rows are retrieved)
    for partij in client.partij.list_iter(max_requests=10):
        print(partij)

Get a specific resource
-----------------------

.. code-block:: python

    # Get a partij by UUID
    partij = client.partij.get(uuid="123e4567-e89b-12d3-a456-426614174000")

Create a resource
-----------------

.. code-block:: python

    # Create a new actor
    actor = client.actor.create(
        data={
            "naam": "John Doe",
            "soortActor": "medewerker",
            "indicatieActief": True,
            "actoridentificator": {
                "objectId": "123456",
                "codeObjecttype": "employee",
                "codeRegister": "hr",
                "codeSoortObjectId": "id",
            },
        }
    )
