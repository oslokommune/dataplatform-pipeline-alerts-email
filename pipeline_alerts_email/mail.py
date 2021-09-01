from okdata.aws.logging import log_exception

import os
import requests


def send_email(message, to_address):
    try:
        # Spec for "EMAIL API" from Team økonomi:
        # https://developer.oslo.kommune.no/katalog/api/31/introduction
        payload = {
            "mottakerepost": [
                to_address,
                # "simen.heggestoyl@origo.oslo.kommune.no",  # WIP
                "jon.morten.kristiansen@origo.oslo.kommune.no",  # WIP
            ],
            "avsenderepost": "dataplattform@oslo.kommune.no",
            "avsendernavn": "Dataplattform",
            "emne": "Feil ved kjøring av pipeline",
            "meldingskropp": message,
        }
        headers = {"apikey": os.environ["EMAIL_API_KEY"]}
        response = requests.post(
            os.environ["EMAIL_API_URL"], data=payload, headers=headers
        )
        response.raise_for_status()

        return {"status_code": response.status_code}
    except requests.RequestException as e:
        log_exception(e)
        return None
