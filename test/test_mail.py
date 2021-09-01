from pipeline_alerts_email.mail import send_email


def test_send_email(requests_mock):
    requests_mock.register_uri("POST", "https://test", text=None, status_code=200)
    response = {"status_code": 200}
    assert send_email("foo", "foo@example.org") == response
