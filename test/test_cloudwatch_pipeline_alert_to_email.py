import json

from email.cloudwatch_pipeline_state_to_email import check_if_status_is_failed

message_mock = {
    "region": "eu-west-1",
    "detail": {
        "name": "Failed Event",
        "status": "FAILED",
        "stateMachineArn": "blabla:blabla:state-machine-1",
        "executionArn": "blabla:blabla:blabla:execution-1",
    },
}

message_mock_wrong_status = {
    "detail": {"name": "Successful Event", "status": "SUCCESS"}
}

message_mock_no_detail = {}


def make_event(message):
    return {
        "Records": [{"EventSource": "aws:sns", "Sns": {"Message": json.dumps(message)}}]
    }


def test_check_if_status_is_failed():
    assert check_if_status_is_failed(message_mock.get("detail")) is True
    assert check_if_status_is_failed(message_mock_wrong_status.get("detail")) is False
