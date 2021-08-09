from unittest.mock import patch

from pipeline_alerts_email.handler import (
    dataset_contact_address,
    get_trace_id,
    handle_message,
    handler,
    has_failed,
    output_dataset,
    pipeline_input,
    record_message,
    trace_error_messages,
)


def test_has_failed_not_failed(message):
    assert not has_failed(message)


def test_has_failed_failed(message_failed):
    assert has_failed(message_failed)


def test_pipeline_input(message):
    p_in = pipeline_input(message)
    assert "pipeline" in p_in
    assert "output_dataset" in p_in
    assert "step_data" in p_in


def test_get_trace_id(message):
    assert (
        get_trace_id(message)
        == "dataplatform-probe-c0e2a8b0-7297-49b4-2a8a-f7afb67c1b09"
    )


def test_output_dataset(message):
    assert output_dataset(message) == "dataplatform-probe"


def test_dataset_contact_address(message):
    with patch("pipeline_alerts_email.handler.Dataset") as Dataset:
        Dataset.return_value.get_dataset.return_value = {
            "contactPoint": {
                "name": "Origo Dataplattform",
                "email": "dataplattform@oslo.kommune.no",
            },
            "Type": "Dataset",
            "Id": "dataplatform-probe",
        }
        assert dataset_contact_address(message) == "dataplattform@oslo.kommune.no"


def test_trace_error_messages(trace):
    assert (
        trace_error_messages(trace)
        == "Operasjon: validate_input\nMeldinger:\n- Opplastet JSON er ugyldig."
    )


def test_record_message(event, message):
    assert record_message(event["Records"][0]) == message


def test_handle_message_not_failed(message):
    with patch("pipeline_alerts_email.handler.send_email") as send_email:
        handle_message(message)
        send_email.assert_not_called()


def test_handle_message_failed(message_failed):
    with patch("pipeline_alerts_email.handler.Status"):
        with patch("pipeline_alerts_email.handler.send_email") as send_email:
            handle_message(message_failed)
            send_email.assert_called_once()


def test_handler(event, message):
    with patch("pipeline_alerts_email.handler.handle_message") as handle_message:
        handler(event, None)
        handle_message.assert_called_once_with(message)
