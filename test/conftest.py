import json

import pytest


@pytest.fixture
def message():
    return {
        "version": "0",
        "id": "b10d3345-db43-4730-ff2f-3257fd510c24",
        "detail-type": "Step Functions Execution Status Change",
        "source": "aws.states",
        "account": "123456789101",
        "time": "2021-08-05T07:47:08Z",
        "region": "eu-west-1",
        "resources": [
            "arn:aws:states:eu-west-1:123456789101:execution:dataplatform-event-copy:dataplatform-probe-c0e2a8b0-7297-49b4-2a8a-f7afb67c1b09"
        ],
        "detail": {
            "executionArn": "arn:aws:states:eu-west-1:123456789101:execution:dataplatform-event-copy:dataplatform-probe-c0e2a8b0-7297-49b4-2a8a-f7afb67c1b09",
            "stateMachineArn": "arn:aws:states:eu-west-1:123456789101:stateMachine:dataplatform-event-copy",
            "name": "dataplatform-probe-c0e2a8b0-7297-49b4-2a8a-f7afb67c1b09",
            "status": "SUCCEEDED",
            "startDate": 1628149627897,
            "stopDate": 1628149628286,
            "input": '{"pipeline":{"id":"dataplatform-probe","task_config":null},"output_dataset":{"id":"dataplatform-probe","version":"1","s3_prefix":""},"step_data":{"input_events":[{"app_id":"f074c2f9","seqno":7909,"time_sent":"2021-08-05T07:47:05.497525+00:00"}],"status":"PENDING","errors":[]}}',
            "inputDetails": {"included": True},
            "output": '{"pipeline":{"id":"dataplatform-probe","task_config":null},"output_dataset":{"id":"dataplatform-probe","version":"1","s3_prefix":""},"step_data":{"status":"OK","errors":[],"s3_input_prefixes":null,"input_events":[{"app_id":"f074c2f9","seqno":7909,"time_sent":"2021-08-05T07:47:05.497525+00:00"}]}}',
            "outputDetails": {"included": True},
        },
    }


@pytest.fixture
def message_failed(message):
    message["detail"]["status"] = "FAILED"
    return message


@pytest.fixture
def event(message):
    return {
        "Records": [{"EventSource": "aws:sns", "Sns": {"Message": json.dumps(message)}}]
    }
