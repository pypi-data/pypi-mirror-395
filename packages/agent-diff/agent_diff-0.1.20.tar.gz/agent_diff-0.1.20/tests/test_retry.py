import pytest
from unittest.mock import patch, MagicMock
import requests

from agent_diff.client import AgentDiff, RETRYABLE_STATUS_CODES


class TestRequestWithRetry:
    def test_success_on_first_attempt(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}

        with patch("requests.request", return_value=mock_response) as mock_request:
            response = client._request_with_retry("POST", "https://api.test.com/test")

            assert response.status_code == 200
            assert mock_request.call_count == 1

    def test_retry_on_502(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        error_response = MagicMock()
        error_response.status_code = 502

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"ok": True}

        with patch("requests.request", side_effect=[error_response, success_response]) as mock_request:
            with patch("time.sleep"):
                response = client._request_with_retry("POST", "https://api.test.com/test")

                assert response.status_code == 200
                assert mock_request.call_count == 2

    def test_retry_on_503(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        error_response = MagicMock()
        error_response.status_code = 503

        success_response = MagicMock()
        success_response.status_code = 200

        with patch("requests.request", side_effect=[error_response, success_response]) as mock_request:
            with patch("time.sleep"):
                response = client._request_with_retry("POST", "https://api.test.com/test")

                assert response.status_code == 200
                assert mock_request.call_count == 2

    def test_retry_on_504(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        error_response = MagicMock()
        error_response.status_code = 504

        success_response = MagicMock()
        success_response.status_code = 200

        with patch("requests.request", side_effect=[error_response, success_response]) as mock_request:
            with patch("time.sleep"):
                response = client._request_with_retry("POST", "https://api.test.com/test")

                assert response.status_code == 200
                assert mock_request.call_count == 2

    def test_retry_on_connection_error(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        success_response = MagicMock()
        success_response.status_code = 200

        with patch(
            "requests.request",
            side_effect=[requests.exceptions.ConnectionError("Connection failed"), success_response],
        ) as mock_request:
            with patch("time.sleep"):
                response = client._request_with_retry("POST", "https://api.test.com/test")

                assert response.status_code == 200
                assert mock_request.call_count == 2

    def test_exhausts_retries_and_raises(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        error_response = MagicMock()
        error_response.status_code = 502
        error_response.raise_for_status.side_effect = requests.HTTPError(response=error_response)

        with patch("requests.request", return_value=error_response) as mock_request:
            with patch("time.sleep"):
                with pytest.raises(requests.HTTPError):
                    client._request_with_retry("POST", "https://api.test.com/test", max_retries=3)

                assert mock_request.call_count == 3

    def test_no_retry_on_400(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        error_response = MagicMock()
        error_response.status_code = 400
        error_response.raise_for_status.side_effect = requests.HTTPError(response=error_response)

        with patch("requests.request", return_value=error_response) as mock_request:
            with pytest.raises(requests.HTTPError):
                client._request_with_retry("POST", "https://api.test.com/test")

            assert mock_request.call_count == 1

    def test_no_retry_on_401(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        error_response = MagicMock()
        error_response.status_code = 401
        error_response.raise_for_status.side_effect = requests.HTTPError(response=error_response)

        with patch("requests.request", return_value=error_response) as mock_request:
            with pytest.raises(requests.HTTPError):
                client._request_with_retry("POST", "https://api.test.com/test")

            assert mock_request.call_count == 1

    def test_exponential_backoff(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        error_response = MagicMock()
        error_response.status_code = 502
        error_response.raise_for_status.side_effect = requests.HTTPError(response=error_response)

        with patch("requests.request", return_value=error_response):
            with patch("time.sleep") as mock_sleep:
                with pytest.raises(requests.HTTPError):
                    client._request_with_retry(
                        "POST", "https://api.test.com/test", max_retries=3, retry_delay=0.5
                    )

                # Should sleep with increasing delays: 0.5, 1.0 (no sleep after last attempt)
                assert mock_sleep.call_count == 2
                mock_sleep.assert_any_call(0.5)
                mock_sleep.assert_any_call(1.0)


class TestInitEnvRetry:
    def test_init_env_uses_retry(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        with patch.object(client, "_request_with_retry") as mock_retry:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "environmentId": "env-123",
                "schema": "test_schema",
            }
            mock_retry.return_value = mock_response

            client.init_env(templateService="linear", templateName="default")

            mock_retry.assert_called_once()
            call_args = mock_retry.call_args
            assert call_args[0][0] == "POST"
            assert "/api/platform/initEnv" in call_args[0][1]


class TestStartRunRetry:
    def test_start_run_uses_retry(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        with patch.object(client, "_request_with_retry") as mock_retry:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "runId": "run-123",
                "status": "running",
                "beforeSnapshot": "snap-123",
            }
            mock_retry.return_value = mock_response

            client.start_run(envId="env-123")

            mock_retry.assert_called_once()
            call_args = mock_retry.call_args
            assert call_args[0][0] == "POST"
            assert "/api/platform/startRun" in call_args[0][1]


class TestEvaluateRunRetry:
    def test_evaluate_run_uses_retry(self):
        client = AgentDiff(api_key="test_key", base_url="https://api.test.com")

        with patch.object(client, "_request_with_retry") as mock_retry:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "runId": "run-123",
                "status": "completed",
            }
            mock_retry.return_value = mock_response

            client.evaluate_run(runId="run-123")

            mock_retry.assert_called_once()
            call_args = mock_retry.call_args
            assert call_args[0][0] == "POST"
            assert "/api/platform/evaluateRun" in call_args[0][1]

