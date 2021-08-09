from unittest.mock import Mock, patch

from pipeline_alerts_email.mail import send_email


def test_send_email():
    response = {"MessageId": 1}
    mock_client = Mock()

    with patch("pipeline_alerts_email.mail.boto3.client") as client:
        client.return_value = mock_client
        mock_client.send_email.return_value = response

        assert send_email("foo", "foo@example.org") == response

        mock_client.send_email.assert_called_once()
