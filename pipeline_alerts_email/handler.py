import json
import logging

from okdata.sdk.data.dataset import Dataset

from pipeline_alerts_email.mail import send_email

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def has_failed(message):
    detail = message.get("detail", {})
    return detail.get("status") in ["ABORTED", "FAILED", "TIMED_OUT"]


def pipeline_input(message):
    detail = message.get("detail", {})
    return json.loads(detail.get("input", "{}"))


def output_dataset(message):
    return pipeline_input(message).get("output_dataset", {}).get("id")


def dataset_contact_address(dataset):
    ds = Dataset().get_dataset(dataset) or {}
    return ds.get("contactPoint", {}).get("email")


def handle_message(message):
    logger.info(f"Handling message: {message}")

    detail_type = message.get("detail-type")
    if detail_type != "Step Functions Execution Status Change":
        logger.info(f"Unexpected message detail-type: {detail_type}, skipping")
        return

    source = message.get("source")
    if source != "aws.states":
        logger.info(f"Unexpected message source: {source}, skipping")
        return

    if not has_failed(message):
        logger.info("Pipeline hasn't failed, skipping")
        return

    dataset = output_dataset(message)
    if not dataset:
        logger.info("Missing output dataset, skipping")
        return

    contact_address = dataset_contact_address(dataset)
    if not contact_address:
        logger.info("Missing dataset contact address, skipping")
        return

    errors = "\n".join(pipeline_input(message).get("step_data", {}).get("errors", []))
    error_message = "Pipelinekjøring for datasett '{}' feilet{}".format(
        dataset, f": \n\n{errors}" if errors else "."
    )

    # WIP
    error_message += f"\n\n(denne skulle ha gått til {contact_address})"
    # WIP

    logger.info(f"Messaging '{contact_address}':\n\n{error_message}")
    send_email(error_message, contact_address)


def record_message(record):
    """Return the message part of the given SNS record."""

    source = record["EventSource"]

    if source != "aws:sns":
        raise ValueError(
            f"Unsupported event source '{source}', only 'aws:sns' is supported."
        )

    return json.loads(record["Sns"]["Message"])


def handler(event, context):
    for r in event["Records"]:
        handle_message(record_message(r))
