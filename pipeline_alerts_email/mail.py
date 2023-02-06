import os
import requests

from okdata.aws.logging import log_exception


def send_email(message, to_address):
    try:
        html_message = message.replace("\n", "<br />")

        email_html_body = (
            f"<p>{html_message}</p>"
            '<p><strong>Ta kontakt med oss på <a href="https://app.slack.com/client/T6W3G5A4C/C01DE13PLDP">Slack</a> eller dataplattform@oslo.kommune.no dersom du trenger hjelp.</strong></p>'
        )

        # Spec for "EMAIL API" from Team økonomi:
        # https://developer.oslo.kommune.no/katalog/api/31/introduction
        payload = {
            "mottakerepost": [
                to_address,
            ],
            "epostbcc": [
                "simen.heggestoyl@origo.oslo.kommune.no",  # WIP
            ],
            "avsenderepost": "dataplattform@oslo.kommune.no",
            "avsendernavn": "Dataplattform",
            "emne": "Feil ved kjøring av pipeline",
            "meldingskropp": email_html_body,
        }
        headers = {"apikey": os.environ["EMAIL_API_KEY"]}
        response = requests.post(
            os.environ["EMAIL_API_URL"], json=payload, headers=headers
        )
        response.raise_for_status()

        return {"status_code": response.status_code}
    except requests.RequestException as e:
        log_exception(e)
        return None
