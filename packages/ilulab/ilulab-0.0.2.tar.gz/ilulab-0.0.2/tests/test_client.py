"""
Basic tests for ilulab Python client.
Run with: uv run pytest
"""

from unittest.mock import Mock, patch

from ilulab.client import IlulabClient, Run


def test_client_initialization():
    """Test client initialization."""
    client = IlulabClient(api_url="http://localhost")
    assert client.api_url == "http://localhost"
    client.close()


def test_client_with_context_manager():
    """Test client can be used as context manager."""
    with IlulabClient(api_url="http://localhost") as client:
        assert client.api_url == "http://localhost"


@patch("ilulab.client.httpx.Client")
def test_create_project(mock_client):
    """Test creating a project."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": "test-id",
        "name": "test-project",
        "description": "Test",
    }
    mock_response.raise_for_status = Mock()
    mock_client_instance = Mock()
    mock_client_instance.post.return_value = mock_response
    mock_client.return_value = mock_client_instance

    client = IlulabClient()
    project = client.create_project(name="test-project", description="Test")

    assert project["name"] == "test-project"
    mock_client_instance.post.assert_called_once()
    client.close()


def test_run_log_param():
    """Test logging a parameter."""
    from uuid import uuid4

    client = IlulabClient()
    run = Run(run_id=uuid4(), client=client)

    with patch.object(client, "_post") as mock_post, patch.object(client, "_patch") as mock_patch:
        mock_post.return_value = {}
        mock_patch.return_value = {}
        run.log_param("learning_rate", 0.001)
        # Params are buffered, flush to send
        run.finish()
        mock_post.assert_called_once()

    client.close()


def test_run_log_params():
    """Test logging multiple parameters."""
    from uuid import uuid4

    client = IlulabClient()
    run = Run(run_id=uuid4(), client=client)

    with patch.object(client, "_post") as mock_post, patch.object(client, "_patch") as mock_patch:
        mock_post.return_value = {}
        mock_patch.return_value = {}
        run.log_params({"learning_rate": 0.001, "batch_size": 32, "optimizer": "adam"})
        # Params are buffered, flush to send
        run.finish()
        mock_post.assert_called_once()

    client.close()


def test_run_log_metric():
    """Test logging a single metric."""
    from uuid import uuid4

    client = IlulabClient()
    run = Run(run_id=uuid4(), client=client)

    with patch.object(client, "_post") as mock_post, patch.object(client, "_patch") as mock_patch:
        mock_post.return_value = {}
        mock_patch.return_value = {}
        run.log_metric("loss", 0.5, step=0)
        # Metrics are buffered, flush to send
        run.finish()
        mock_post.assert_called_once()

    client.close()


def test_run_log_metrics():
    """Test logging multiple metrics."""
    from uuid import uuid4

    client = IlulabClient()
    run = Run(run_id=uuid4(), client=client)

    with patch.object(client, "_post") as mock_post, patch.object(client, "_patch") as mock_patch:
        mock_post.return_value = {}
        mock_patch.return_value = {}
        run.log_metrics({"loss": 0.5, "accuracy": 0.8}, step=0)
        # Metrics are buffered, flush to send
        run.finish()
        mock_post.assert_called_once()

    client.close()


def test_run_auto_step():
    """Test auto-incrementing step counter."""
    from uuid import uuid4

    client = IlulabClient()
    run = Run(run_id=uuid4(), client=client)

    with patch.object(client, "_post") as mock_post, patch.object(client, "_patch") as mock_patch:
        mock_post.return_value = {}
        mock_patch.return_value = {}

        # Log two metrics without explicit step
        run.log_metric("loss", 0.5)
        run.log_metric("loss", 0.4)

        # Check buffer contents directly for step values
        assert run._metrics_buffer[0]["step"] == 0
        assert run._metrics_buffer[1]["step"] == 1

        run.finish()

    client.close()


def test_run_context_manager():
    """Test Run can be used as context manager."""
    from uuid import uuid4

    client = IlulabClient()
    run_id = uuid4()
    run = Run(run_id=run_id, client=client)

    with patch.object(client, "_patch") as mock_patch, patch.object(client, "_post") as mock_post:
        mock_patch.return_value = {}
        mock_post.return_value = {}

        with run:
            pass

        # Should mark as completed on exit
        mock_patch.assert_called_once()
        args = mock_patch.call_args[0]
        assert "completed" in str(args)

    client.close()


def test_client_close_flushes_active_runs():
    """Test that closing the client flushes buffers of active runs."""
    from uuid import uuid4

    client = IlulabClient()
    run = Run(run_id=uuid4(), client=client)
    client._active_runs.append(run)

    with patch.object(client, "_post") as mock_post:
        mock_post.return_value = {}

        # Log some metrics (buffered, not sent yet)
        run.log_metric("loss", 0.5, step=0)
        assert len(run._metrics_buffer) == 1

        # Close client should flush the buffer
        client.close()

        # Buffer should be flushed
        assert len(run._metrics_buffer) == 0
        mock_post.assert_called_once()


def test_run_finish_removes_from_active_runs():
    """Test that finishing a run removes it from client's active runs."""
    from uuid import uuid4

    client = IlulabClient()
    run = Run(run_id=uuid4(), client=client)
    client._active_runs.append(run)

    with patch.object(client, "_post") as mock_post, patch.object(client, "_patch") as mock_patch:
        mock_post.return_value = {}
        mock_patch.return_value = {}

        assert run in client._active_runs
        run.finish()
        assert run not in client._active_runs

    client.close()
