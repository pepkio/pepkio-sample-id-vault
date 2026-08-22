"""Unit tests with mocked HTTP."""

from __future__ import annotations

import json

import httpx
import pytest

from pepkio_sample_id_vault.client import PepkioClient
from pepkio_sample_id_vault.config import TOOL_ID
from pepkio_sample_id_vault.exceptions import PepkioAPIError
from pepkio_sample_id_vault.models import RunResult


def _make_client(handler) -> PepkioClient:
    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key", base_url="https://tools.example.com")
    client._http = httpx.Client(
        base_url=client.base_url,
        headers={"Authorization": "Bearer test-key"},
        transport=transport,
        timeout=30.0,
    )
    return client


def test_get_manifest_and_cache(mock_manifest):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        assert request.url.path == f"/api/tools/v1/tools/{TOOL_ID}/manifest"
        return httpx.Response(200, json=mock_manifest)

    with _make_client(handler) as client:
        m1 = client.get_manifest()
        m2 = client.get_manifest()
        assert m1["tool_id"] == "sample-id-vault"
        assert m1 is m2
    assert len(calls) == 1


def test_get_manifest_refresh(mock_manifest):
    count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal count
        count += 1
        return httpx.Response(200, json=mock_manifest)

    with _make_client(handler) as client:
        client.get_manifest()
        client.get_manifest(refresh=True)
    assert count == 2


def test_list_examples_and_get_example_input(mock_manifest):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=mock_manifest)

    with _make_client(handler) as client:
        names = client.list_examples()
        assert "generate_reversible" in names
        inp = client.get_example_input("generate_reversible")
        assert inp["action"] == "generate"
        assert inp["mode"] == "reversible"


def test_get_example_input_not_found(mock_manifest):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=mock_manifest)

    with _make_client(handler) as client:
        client.get_manifest()
        with pytest.raises(PepkioAPIError, match="not found"):
            client.get_example_input("missing")


def test_run_sends_correct_request(mock_manifest, mock_run_response):
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/manifest"):
            return httpx.Response(200, json=mock_manifest)
        captured["path"] = request.url.path
        captured["auth"] = request.headers.get("Authorization")
        captured["body"] = json.loads(request.content.decode())
        return httpx.Response(200, json=mock_run_response)

    with _make_client(handler) as client:
        result = client.run(client.get_example_input("generate_reversible"), label="pytest")

    assert captured["path"] == f"/api/tools/v1/tools/{TOOL_ID}/run"
    assert captured["auth"] == "Bearer test-key"
    assert captured["body"]["input"]["action"] == "generate"
    assert captured["body"]["options"]["label"] == "pytest"
    assert result.status == "completed"


def test_run_requires_api_key(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)
    client = PepkioClient(api_key=None, base_url="https://tools.example.com")
    with pytest.raises(ValueError, match="API key required"):
        client.run({"action": "generate"})


def test_http_401_raises_api_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401,
            json={"error": {"code": "UNAUTHORIZED", "message": "Invalid API key", "details": {}}},
        )

    with _make_client(handler) as client:
        with pytest.raises(PepkioAPIError) as exc:
            client.run({"action": "generate"})
        assert exc.value.status_code == 401
        assert exc.value.code == "UNAUTHORIZED"


def test_http_400_validation_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input",
                    "details": {"issues": {}},
                }
            },
        )

    with _make_client(handler) as client:
        with pytest.raises(PepkioAPIError) as exc:
            client.run({})
        assert exc.value.code == "VALIDATION_ERROR"


def test_run_response_error_field(mock_run_response):
    body = {**mock_run_response, "error": {"code": "TOOL_FAILED", "message": "processing error"}}

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=body)

    with _make_client(handler) as client:
        with pytest.raises(PepkioAPIError, match="processing error"):
            client.run({"action": "generate"})


def test_raise_for_error_on_run_result():
    r = RunResult(
        run_id="x",
        status="failed",
        error={"code": "TOOL_FAILED", "message": "failed"},
    )
    with pytest.raises(PepkioAPIError):
        r.raise_for_error()


def test_get_run(mock_run_response):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run_test123"
        return httpx.Response(200, json=mock_run_response)

    with _make_client(handler) as client:
        result = client.get_run("run_test123")
        assert result.run_id == "run_test123"


def test_wait_for_run(mock_run_response):
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(200, json={"run_id": "run_test123", "status": "running"})
        return httpx.Response(200, json=mock_run_response)

    with _make_client(handler) as client:
        result = client.wait_for_run("run_test123", poll_interval=0.01, timeout=5.0)
        assert result.status == "completed"
    assert calls == 2
