"""Tests for demo_app.claim_files: loading, validating, and finding claim files."""
import json

import pytest

from demo_app.claim_files import (
    InvalidClaimFileError,
    build_message,
    find_claim_files,
    load_claim_file,
)


def test_load_claim_file_reads_valid_json(tmp_path):
    path = tmp_path / "claim.json"
    path.write_text(json.dumps({"claim_id": "C-1", "category": "water", "amount": 5000}))

    claim = load_claim_file(path)

    assert claim == {"claim_id": "C-1", "category": "water", "amount": 5000}


def test_load_claim_file_rejects_invalid_json(tmp_path):
    path = tmp_path / "claim.json"
    path.write_text("{not valid json")

    with pytest.raises(InvalidClaimFileError):
        load_claim_file(path)


def test_load_claim_file_rejects_missing_required_fields(tmp_path):
    path = tmp_path / "claim.json"
    path.write_text(json.dumps({"claim_id": "C-1"}))

    with pytest.raises(InvalidClaimFileError, match="category"):
        load_claim_file(path)


def test_build_message_uses_explicit_message_if_present():
    claim = {"category": "auto", "amount": 5000, "message": "custom message here"}
    assert build_message(claim) == "custom message here"


def test_build_message_synthesizes_from_category_and_amount():
    claim = {"category": "water", "amount": 5000}
    message = build_message(claim)
    assert "water" in message
    assert "5000" in message


def test_build_message_includes_description_when_present():
    claim = {"category": "auto", "amount": 5000, "description": "fender bender"}
    message = build_message(claim)
    assert "fender bender" in message


def test_find_claim_files_expands_a_directory(tmp_path):
    (tmp_path / "a.json").write_text("{}")
    (tmp_path / "b.json").write_text("{}")
    (tmp_path / "c.txt").write_text("not json")

    files = find_claim_files([str(tmp_path)])

    assert sorted(f.name for f in files) == ["a.json", "b.json"]


def test_find_claim_files_accepts_individual_files(tmp_path):
    path = tmp_path / "claim.json"
    path.write_text("{}")

    files = find_claim_files([str(path)])

    assert files == [path]


def test_find_claim_files_rejects_a_path_that_does_not_exist(tmp_path):
    with pytest.raises(InvalidClaimFileError):
        find_claim_files([str(tmp_path / "nope.json")])
