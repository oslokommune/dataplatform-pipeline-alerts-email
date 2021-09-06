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


@pytest.fixture
def trace():
    return [
        {
            "trace_event_status": "OK",
            "operation": "upload",
            "component": "data-uploader",
            "s3_path": "raw/green/my-dataset/version=1/edition=20210809T122237/input_bad.json",
            "user": "foo",
            "start_time": "2021-08-09T12:22:41.743989+00:00",
            "end_time": "2021-08-09T12:22:42.037621+00:00",
            "trace_id": "my-dataset-7d5ca7f7-8ec1-6eaf-0cfd-72525a882417",
            "trace_status": "STARTED",
            "domain_id": "my-dataset/1",
            "trace_event_id": "43c779d2-c94c-c964-e7b7-5f7d9589b7e5",
            "domain": "dataset",
        },
        {
            "trace_event_status": "OK",
            "operation": "validate_input",
            "component": "okdata-pipeline",
            "meta": {
                "git_rev": "main:bc7d428",
                "function_name": "okdata-pipeline-dev-validate-json",
                "function_version": "$LATEST",
            },
            "start_time": "2021-08-09T12:22:58.263737+00:00",
            "end_time": "2021-08-09T12:22:58.356359+00:00",
            "trace_id": "my-dataset-7d5ca7f7-8ec1-6eaf-0cfd-72525a882417",
            "trace_status": "CONTINUE",
            "errors": [
                {
                    "message": {
                        "nb": "Opplastet JSON er ugyldig.",
                        "en": "Uploaded JSON is invalid.",
                    },
                }
            ],
            "domain_id": "my-dataset/1",
            "trace_event_id": "9bca5a33-c3c3-dc24-5804-d87388f220fa",
            "duration": 92,
            "domain": "dataset",
        },
        {
            "trace_event_status": "FAILED",
            "operation": "set_finished_status",
            "component": "state-machine-event",
            "trace_status": "FINISHED",
            "meta": {
                "git_rev": "main:784b55d",
                "function_name": "state-machine-event-dev-act_on_queue",
                "function_version": "$LATEST",
            },
            "start_time": "2021-08-09T12:22:59.906946+00:00",
            "trace_event_id": "71d061f0-0014-0024-31f9-2dbe6b8e782d",
            "end_time": "2021-08-09T12:22:59.907352+00:00",
            "trace_id": "my-dataset-7d5ca7f7-8ec1-6eaf-0cfd-72525a882417",
            "domain": "dataset",
        },
    ]


@pytest.fixture
def dataset():
    return {
        "contactPoint": {
            "name": "Origo Dataplattform",
            "email": "dataplattform@oslo.kommune.no",
        },
        "Type": "Dataset",
        "Id": "dataplatform-probe",
    }
