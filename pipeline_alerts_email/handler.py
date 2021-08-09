import json

from okdata.aws.logging import log_add, logging_wrapper
from okdata.sdk.data.dataset import Dataset

from pipeline_alerts_email.mail import send_email


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
    log_add(sent=False)

    detail_type = message.get("detail-type")
    if detail_type != "Step Functions Execution Status Change":
        log_add(skip_reason=f"Unexpected message detail-type: {detail_type}")
        return

    source = message.get("source")
    if source != "aws.states":
        log_add(skip_reason=f"Unexpected message source: {source}")
        return

    if not has_failed(message):
        log_add(skip_reason="Pipeline hasn't failed")
        return

    dataset = output_dataset(message)
    if not dataset:
        log_add(skip_reason="Missing output dataset")
        return

    contact_address = dataset_contact_address(dataset)
    if not contact_address:
        log_add(skip_reason="Missing dataset contact address")
        return

    errors = "\n".join(pipeline_input(message).get("step_data", {}).get("errors", []))
    error_message = "Pipelinekjøring for datasett '{}' feilet{}".format(
        dataset, f": \n\n{errors}" if errors else "."
    )

    # WIP
    error_message += f"\n\n(denne skulle ha gått til {contact_address})"
    # WIP

    log_add(error_message=error_message)
    log_add(contact_address=contact_address)

    if send_email(error_message, contact_address):
        log_add(sent=True)


def record_message(record):
    """Return the message part of the given SNS record."""

    source = record["EventSource"]

    if source != "aws:sns":
        raise ValueError(
            f"Unsupported event source '{source}', only 'aws:sns' is supported."
        )

    return json.loads(record["Sns"]["Message"])


@logging_wrapper
def handler(event, context):
    for r in event["Records"]:
        handle_message(record_message(r))
