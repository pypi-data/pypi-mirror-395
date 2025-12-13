"""Main client for interacting with ilulab API."""

import os
import threading
from typing import Any
from uuid import UUID

import httpx


class Run:
    """Represents an ML experiment run with logging capabilities.

    Metrics and parameters are buffered locally and flushed asynchronously
    in batches to avoid blocking the training loop.
    """

    def __init__(
        self,
        run_id: UUID,
        client: "IlulabClient",
        flush_interval: float = 5.0,
        buffer_size: int = 100,
    ):
        """Initialize a Run instance.

        Args:
            run_id: UUID of the run
            client: IlulabClient instance for API communication
            flush_interval: Seconds between automatic flushes (default 5.0)
            buffer_size: Max buffered items before triggering flush (default 100)
        """
        self.run_id = run_id
        self.client = client
        self._current_step = 0

        self._flush_interval = flush_interval
        self._buffer_size = buffer_size
        self._metrics_buffer: list[dict] = []
        self._params_buffer: list[dict] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()

    def _flush_loop(self) -> None:
        """Background thread that periodically flushes buffers."""
        while not self._stop_event.wait(self._flush_interval):
            self._flush()
        # Final flush when stopping
        self._flush()

    def _flush(self) -> None:
        """Flush buffered metrics and parameters to the API."""
        with self._lock:
            metrics_to_send = self._metrics_buffer[:]
            params_to_send = self._params_buffer[:]
            self._metrics_buffer.clear()
            self._params_buffer.clear()

        if metrics_to_send:
            self.client._post(
                f"/api/metrics/{self.run_id}/batch",
                {"metrics": metrics_to_send},
            )
        if params_to_send:
            self.client._post(f"/api/parameters/{self.run_id}/batch", params_to_send)

    def _maybe_flush(self) -> None:
        """Trigger flush if buffer size exceeded."""
        with self._lock:
            should_flush = (
                len(self._metrics_buffer) >= self._buffer_size
                or len(self._params_buffer) >= self._buffer_size
            )
        if should_flush:
            self._flush()

    def log_param(self, key: str, value: str | float | int) -> None:
        """Log a parameter (configuration value) for this run.

        Args:
            key: Parameter name
            value: Parameter value (string or numeric)
        """
        if isinstance(value, (int, float)):
            param = {"key": key, "value_numeric": float(value)}
        else:
            param = {"key": key, "value_string": str(value)}

        with self._lock:
            self._params_buffer.append(param)
        self._maybe_flush()

    def log_params(self, params: dict[str, str | float | int]) -> None:
        """Log multiple parameters at once.

        Args:
            params: Dictionary of parameter names to values
        """
        param_list = []
        for key, value in params.items():
            if isinstance(value, (int, float)):
                param_list.append({"key": key, "value_numeric": float(value)})
            else:
                param_list.append({"key": key, "value_string": str(value)})

        with self._lock:
            self._params_buffer.extend(param_list)
        self._maybe_flush()

    def log_metric(self, key: str, value: float, step: int | None = None) -> None:
        """Log a metric value at a specific step.

        Args:
            key: Metric name (e.g., 'loss', 'accuracy')
            value: Metric value
            step: Training step/epoch (defaults to auto-incrementing counter)
        """
        if step is None:
            step = self._current_step
            self._current_step += 1

        metric = {"key": key, "value": float(value), "step": step}
        with self._lock:
            self._metrics_buffer.append(metric)
        self._maybe_flush()

    def log_metrics(self, metrics: dict[str, float], step: int | None = None) -> None:
        """Log multiple metrics at the same step.

        Args:
            metrics: Dictionary of metric names to values
            step: Training step/epoch (defaults to auto-incrementing counter)
        """
        if step is None:
            step = self._current_step
            self._current_step += 1

        metric_list = [
            {"key": key, "value": float(value), "step": step} for key, value in metrics.items()
        ]

        with self._lock:
            self._metrics_buffer.extend(metric_list)
        self._maybe_flush()

    def set_step(self, step: int) -> None:
        """Set the current step counter.

        Args:
            step: Step number to set
        """
        self._current_step = step

    def add_tag(self, tag: str) -> None:
        """Add a tag to this run.

        Args:
            tag: Tag name
        """
        self.client._post(f"/api/runs/{self.run_id}/tags/{tag}", {})

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from this run.

        Args:
            tag: Tag name
        """
        self.client._delete(f"/api/runs/{self.run_id}/tags/{tag}")

    def finish(self, status: str = "completed") -> None:
        """Mark the run as finished.

        Stops the background flush thread, flushes any remaining buffered data,
        and updates the run status.

        Args:
            status: Final status ('completed' or 'failed')
        """
        self._stop_event.set()
        self._flush_thread.join(timeout=10.0)
        self._flush()
        self.client._patch(
            f"/api/runs/{self.run_id}",
            {"status": status},
        )
        if self in self.client._active_runs:
            self.client._active_runs.remove(self)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto-finish run."""
        if exc_type is not None:
            self.finish(status="failed")
        else:
            self.finish(status="completed")


class IlulabClient:
    """Client for interacting with the ilulab API."""

    def __init__(self, api_url: str = "https://ilulab.com", token: str | None = None):
        """Initialize the ilulab client.

        Args:
            api_url: Base URL of the ilulab API
            token: Bearer token for authentication (falls back to ILULAB_TOKEN env var)
        """
        self.api_url = api_url.rstrip("/")
        token = token or os.environ.get("ILULAB_TOKEN")
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.client = httpx.Client(base_url=self.api_url, timeout=30.0, headers=headers)
        self._active_runs: list[Run] = []

    def _post(self, endpoint: str, data: Any) -> dict:
        """Make a POST request to the API."""
        response = self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    def _get(self, endpoint: str, params: dict | None = None) -> dict | list:
        """Make a GET request to the API."""
        response = self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def _patch(self, endpoint: str, data: Any) -> dict:
        """Make a PATCH request to the API."""
        response = self.client.patch(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint: str) -> None:
        """Make a DELETE request to the API."""
        response = self.client.delete(endpoint)
        response.raise_for_status()

    def create_project(self, name: str, description: str | None = None) -> dict:
        """Create a new project.

        Args:
            name: Project name
            description: Optional project description

        Returns:
            Project data including ID
        """
        return self._post(
            "/api/projects",
            {"name": name, "description": description},
        )

    def get_project(self, project_id: UUID | str) -> dict:
        """Get project by ID.

        Args:
            project_id: Project UUID

        Returns:
            Project data
        """
        return self._get(f"/api/projects/{project_id}")

    def list_projects(self) -> list[dict]:
        """List all projects.

        Returns:
            List of projects
        """
        return self._get("/api/projects")

    def create_run(
        self,
        project_id: UUID | str,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
    ) -> Run:
        """Create a new experiment run.

        Args:
            project_id: Project UUID
            name: Optional run name
            description: Optional run description
            tags: Optional list of tags

        Returns:
            Run instance for logging metrics and parameters
        """
        data = {
            "project_id": str(project_id),
            "name": name,
            "description": description,
            "tags": tags,
        }
        response = self._post("/api/runs", data)
        run = Run(UUID(response["id"]), self)
        self._active_runs.append(run)
        return run

    def get_run(self, run_id: UUID | str) -> dict:
        """Get run details including all metrics and parameters.

        Args:
            run_id: Run UUID

        Returns:
            Run data with metrics and parameters
        """
        return self._get(f"/api/runs/{run_id}")

    def list_runs(
        self,
        project_id: UUID | str | None = None,
        tag: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        """List runs with optional filtering.

        Args:
            project_id: Filter by project
            tag: Filter by tag
            status: Filter by status

        Returns:
            List of runs
        """
        params = {}
        if project_id:
            params["project_id"] = str(project_id)
        if tag:
            params["tag"] = tag
        if status:
            params["status"] = status

        return self._get("/api/runs", params=params)

    def close(self) -> None:
        """Close the HTTP client.

        Flushes any remaining buffered data from active runs before closing.
        Note: This only flushes data, it does not finish the runs.
        """
        for run in self._active_runs:
            run._stop_event.set()
            run._flush_thread.join(timeout=10.0)
        self._active_runs.clear()
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
