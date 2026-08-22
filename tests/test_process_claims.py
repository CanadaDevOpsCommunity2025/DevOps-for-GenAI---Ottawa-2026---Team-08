"""Tests for demo_app.scenarios.process_claims."""
import json
from unittest.mock import MagicMock, patch

from demo_app.scenarios.process_claims import process_claim_file


@patch("demo_app.scenarios.process_claims.handle_claim")
@patch("demo_app.scenarios.process_claims.get_client")
def test_process_claim_file_upserts_the_claim_and_runs_handle_claim(mock_get_client, mock_handle_claim, tmp_path):
    path = tmp_path / "claim.json"
    path.write_text(json.dumps({"claim_id": "C-9", "category": "water", "amount": 15000, "description": "test"}))

    mock_handle_claim.return_value = {"status": "ok", "tool_name": "escalate_claim", "result": {}}
    client = MagicMock()
    mock_get_client.return_value = client

    result = process_claim_file(path)

    client.table.assert_called_with("claims")
    client.table.return_value.upsert.assert_called_once()
    upserted = client.table.return_value.upsert.call_args[0][0]
    assert upserted["claim_id"] == "C-9"
    assert upserted["status"] == "pending"

    mock_handle_claim.assert_called_once()
    call_args = mock_handle_claim.call_args[0]
    assert call_args[0] == "C-9"
    assert "water" in call_args[1]

    assert result["status"] == "ok"
    assert result["claim_id"] == "C-9"
    assert result["file"] == str(path)
