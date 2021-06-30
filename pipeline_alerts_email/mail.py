import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_email(message, to_address):
    client = boto3.client("ses", region_name="eu-west-1")

    try:
        response = client.send_email(
            Destination={
                # "ToAddresses": [to_address],
                # WIP
                "ToAddresses": ["simen.heggestoyl@origo.oslo.kommune.no"],
                # WIP
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": message,
                    },
                },
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": "Feil ved kjøring av pipeline",
                },
            },
            Source="dataplattform@oslo.kommune.no",
        )
    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        logger.error(f"Error sending email: {error_message}")
        return None

    message_id = response["MessageId"]
    logger.info(f"Email sent. Message ID: {message_id}")
    return response
