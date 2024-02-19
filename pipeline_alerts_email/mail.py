import os

import requests
from okdata.aws.logging import log_exception
from okdata.aws.ssm import get_secret


def send_email(message, to_address):
    try:
        html_message = message.replace("\n", "<br />")

        email_html_body = (
            f"<p>{html_message}</p>"
            '<p><strong>Ta kontakt med oss på <a href="https://app.slack.com/client/T6W3G5A4C/C01DE13PLDP">Slack</a> eller dataplattform@oslo.kommune.no dersom du trenger hjelp.</strong></p>'
        )

        payload = {
            "mottakerepost": [
                to_address,
            ],
            "avsenderepost": "dataplattform@oslo.kommune.no",
            "avsendernavn": "Dataplattform",
            "emne": "Feil ved kjøring av pipeline",
            "meldingskropp": email_html_body,
        }
        headers = {"apikey": get_secret("/dataplatform/shared/email-api-key")}
        response = requests.post(
            os.environ["EMAIL_API_URL"], json=payload, headers=headers
        )
        response.raise_for_status()

        return {"status_code": response.status_code}
    except requests.RequestException as e:
        log_exception(e)
        return None
