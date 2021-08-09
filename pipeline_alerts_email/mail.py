from okdata.aws.logging import log_exception

import boto3
from botocore.exceptions import ClientError


def send_email(message, to_address):
    client = boto3.client("ses", region_name="eu-west-1")

    try:
        return client.send_email(
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
        log_exception(e)
        return None
