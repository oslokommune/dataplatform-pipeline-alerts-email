import json

from okdata.aws.logging import log_add, logging_wrapper
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.status.status import Status
from requests.exceptions import HTTPError, RetryError

from pipeline_alerts_email.mail import send_email


def has_failed(message):
    detail = message.get("detail", {})
    return detail.get("status") in ["ABORTED", "FAILED", "TIMED_OUT"]


def pipeline_input(message):
    detail = message.get("detail", {})
    return json.loads(detail.get("input", "{}"))


def get_trace_id(message):
    return message.get("detail", {}).get("name")


def output_dataset(message):
    return pipeline_input(message).get("output_dataset", {}).get("id")


def dataset_contact_address(dataset):
    ds = Dataset().get_dataset(dataset) or {}
    return ds.get("contactPoint", {}).get("email")


def trace_error_messages(trace):
    def event_error_messages(errors):
        for msg in [e["message"] for e in errors if "message" in e]:
            if "nb" in msg:
                yield msg["nb"]
            elif "en" in msg:
                # Fall back to English in case the Norwegian error message
                # is missing. TODO: The language should ideally be decided
                # based on the preference of the receiver.
                yield msg["en"]

    return "\n\n".join(
        "Operasjon: {}\nMeldinger:\n{}".format(
            event["operation"],
            "\n".join(f"- {msg}" for msg in event_error_messages(event["errors"])),
        )
        for event in trace
        if "errors" in event
    )


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

    try:
        errors = trace_error_messages(Status().get_status(get_trace_id(message)))
    except (HTTPError, RetryError):
        # Don't try too hard getting the status trace. If the status API is
        # unavaiable or unable to look up the trace ID for some reason, just
        # don't include the error messages.
        errors = []

    error_message = "Pipelinekjøring for datasett '{}' feilet.{}".format(
        dataset, f"\n\n{errors}" if errors else ""
    )

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
