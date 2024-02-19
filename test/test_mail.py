from unittest.mock import patch

from pipeline_alerts_email.mail import send_email


def test_send_email(requests_mock):
    requests_mock.register_uri("POST", "https://test", text=None, status_code=200)
    with patch("pipeline_alerts_email.mail.get_secret") as get_secret:
        get_secret.return_value = "test"
        assert send_email("foo", "foo@example.org") == {"status_code": 200}
