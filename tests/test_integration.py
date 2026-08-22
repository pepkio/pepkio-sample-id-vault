"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_sample_id_vault.client import PepkioClient

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "sample-id-vault"
    names = live_client.list_examples()
    assert "generate_reversible" in names
    assert "generate_irreversible" in names
    assert "parse_csv" in names


def test_run_generate_reversible(live_client: PepkioClient):
    inp = live_client.get_example_input("generate_reversible")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert isinstance(result.result.get("rows"), list)
    assert len(result.result["rows"]) > 0


def test_run_generate_irreversible(live_client: PepkioClient):
    inp = live_client.get_example_input("generate_irreversible")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.result is not None
    assert isinstance(result.result.get("rows"), list)


def test_run_parse_csv(live_client: PepkioClient):
    inp = live_client.get_example_input("parse_csv")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("row_count") == 2


def test_run_lookup_with_vault(live_client: PepkioClient):
    inp = live_client.get_example_input("lookup_with_vault")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert isinstance(result.result.get("rows"), list)


def test_run_build_audit_log(live_client: PepkioClient):
    inp = live_client.get_example_input("build_audit_log")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None


def test_get_run(live_client: PepkioClient):
    inp = live_client.get_example_input("generate_reversible")
    run_res = live_client.run(inp)
    assert run_res.run_id
    fetched = live_client.get_run(run_res.run_id)
    assert fetched.run_id == run_res.run_id
    assert fetched.status == "completed"
