import json


def check_if_status_is_failed(details):
    status = details.get("status")
    failed_statuses = ["ABORTED", "FAILED", "TIMED_OUT"]

    return status in failed_statuses


def handle_message(message):
    details = message.get("detail", None)
    if not details:
        return False

    if check_if_status_is_failed(details):
        # TODO: Implement sending email
        pass

    return True


def handler(event, context):
    records = event.get("Records", None)
    if not records:
        raise ValueError("Event does not contain Records")
    record = records[0]
    source = record["EventSource"]
    if source == "aws:sns":
        sns = record["Sns"]
        event = json.loads(sns["Message"])
        return handle_message(event)
    else:
        raise ValueError(
            f"Unsuported 'EventSource' {source}. Supported types: 'aws:sns'"
        )
