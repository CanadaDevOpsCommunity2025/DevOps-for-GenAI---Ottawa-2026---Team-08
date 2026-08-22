"""Tests for demo_app.scenarios.process_claims."""
import json
from unittest.mock import MagicMock, patch

from demo_app.scenarios.process_claims import main, process_claim_file


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


@patch("demo_app.scenarios.process_claims.SupabaseReporter")
@patch("demo_app.scenarios.process_claims.configure")
@patch("demo_app.scenarios.process_claims.find_claim_files")
@patch("demo_app.scenarios.process_claims.process_claim_file")
def test_main_calls_configure_with_supabase_reporter(
    mock_process_claim_file, mock_find_claim_files, mock_configure, mock_supabase_reporter, tmp_path
):
    """Test that main() calls configure(SupabaseReporter()) at startup."""
    # Setup mock files
    files = [tmp_path / "claim1.json"]
    mock_find_claim_files.return_value = files
    mock_process_claim_file.return_value = {"status": "ok", "claim_id": "C-1"}

    main(["some_path"])

    # Assert configure was called once with a SupabaseReporter instance
    mock_configure.assert_called_once()
    call_args = mock_configure.call_args[0]
    assert isinstance(call_args[0], type(mock_supabase_reporter.return_value))


@patch("demo_app.scenarios.process_claims.process_claim_file")
@patch("demo_app.scenarios.process_claims.find_claim_files")
def test_main_continues_processing_after_a_file_fails(mock_find_claim_files, mock_process_claim_file, tmp_path):
    """Test that when one file fails, the batch continues and other files are still processed."""
    # Setup three mock files
    files = [tmp_path / "claim1.json", tmp_path / "claim2.json", tmp_path / "claim3.json"]
    mock_find_claim_files.return_value = files

    # Middle file raises, others succeed
    mock_process_claim_file.side_effect = [
        {"status": "ok", "claim_id": "C-1", "file": str(files[0])},
        Exception("Something went wrong"),
        {"status": "ok", "claim_id": "C-3", "file": str(files[2])},
    ]

    with patch("demo_app.scenarios.process_claims.configure"):
        with patch("demo_app.scenarios.process_claims.SupabaseReporter"):
            # main() should not crash
            main(["some_path"])

    # All three files should have been attempted
    assert mock_process_claim_file.call_count == 3


@patch("demo_app.scenarios.process_claims.process_claim_file")
@patch("demo_app.scenarios.process_claims.find_claim_files")
def test_main_reports_failure_count_in_summary(mock_find_claim_files, mock_process_claim_file, tmp_path, capsys):
    """Test that the failure count appears in the final summary when files fail."""
    # Setup three mock files
    files = [tmp_path / "claim1.json", tmp_path / "claim2.json", tmp_path / "claim3.json"]
    mock_find_claim_files.return_value = files

    # Middle file raises, others succeed
    mock_process_claim_file.side_effect = [
        {"status": "ok", "claim_id": "C-1", "file": str(files[0])},
        Exception("Something went wrong"),
        {"status": "ok", "claim_id": "C-3", "file": str(files[2])},
    ]

    with patch("demo_app.scenarios.process_claims.configure"):
        with patch("demo_app.scenarios.process_claims.SupabaseReporter"):
            main(["some_path"])

    # Check the printed output
    captured = capsys.readouterr()
    output = captured.out + captured.err

    # Should mention that 2 succeeded and 1 failed
    assert "2" in output and "failed" in output.lower()
