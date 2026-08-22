"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "sample-id-vault",
        "title": "Sample ID Vault",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "generate_reversible",
                "input": {
                    "action": "generate",
                    "names_text": "Patient-001 Smith\nPatient-002 Jones\nControl-Alpha\n",
                    "id_length": 6,
                    "prefix": "PAT-",
                    "study_salt": "demo-study-salt-2026",
                    "mode": "reversible",
                },
                "output": {"skipped_blank": 0},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "rows": [
                {"name": "Patient-001 Smith", "id": "PAT-HSWFQZ", "status": "new"},
            ],
            "skipped_blank": 0,
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
