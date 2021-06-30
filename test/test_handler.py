from unittest.mock import patch

from pipeline_alerts_email.handler import (
    dataset_contact_address,
    handle_message,
    handler,
    has_failed,
    output_dataset,
    pipeline_input,
    record_message,
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


def test_record_message(event, message):
    assert record_message(event["Records"][0]) == message


def test_handle_message_not_failed(message):
    with patch("pipeline_alerts_email.handler.send_email") as send_email:
        handle_message(message)
        send_email.assert_not_called()


def test_handle_message_failed(message_failed):
    with patch("pipeline_alerts_email.handler.send_email") as send_email:
        handle_message(message_failed)
        send_email.assert_called_once()


def test_handler(event, message):
    with patch("pipeline_alerts_email.handler.handle_message") as handle_message:
        handler(event, None)
        handle_message.assert_called_once_with(message)
