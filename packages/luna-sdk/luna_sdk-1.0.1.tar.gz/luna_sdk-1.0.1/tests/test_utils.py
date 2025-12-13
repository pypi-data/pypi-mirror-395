"""Tests for utility functions."""

import pytest

from luna.utils import (
    generate_request_id,
    deep_merge,
    omit,
    pick,
    is_retryable_status,
    mask_sensitive,
    validate_id,
)


class TestGenerateRequestId:
    """Tests for request ID generation."""

    def test_generates_unique_ids(self) -> None:
        """Should generate unique IDs."""
        id1 = generate_request_id()
        id2 = generate_request_id()
        
        assert id1.startswith("req_")
        assert id2.startswith("req_")
        assert id1 != id2


class TestDeepMerge:
    """Tests for deep merge."""

    def test_merge_flat_dicts(self) -> None:
        """Should merge flat dictionaries."""
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        
        result = deep_merge(base, override)
        
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_merge_nested_dicts(self) -> None:
        """Should merge nested dictionaries."""
        base = {"a": 1, "b": {"c": 2, "d": 3}}
        override = {"b": {"d": 4, "e": 5}}
        
        result = deep_merge(base, override)
        
        assert result == {"a": 1, "b": {"c": 2, "d": 4, "e": 5}}


class TestOmit:
    """Tests for omit function."""

    def test_omit_keys(self) -> None:
        """Should omit specified keys."""
        obj = {"a": 1, "b": 2, "c": 3}
        result = omit(obj, ["b"])
        
        assert result == {"a": 1, "c": 3}


class TestPick:
    """Tests for pick function."""

    def test_pick_keys(self) -> None:
        """Should pick specified keys."""
        obj = {"a": 1, "b": 2, "c": 3}
        result = pick(obj, ["a", "c"])
        
        assert result == {"a": 1, "c": 3}


class TestIsRetryableStatus:
    """Tests for retryable status check."""

    def test_retryable_statuses(self) -> None:
        """Should identify retryable statuses."""
        assert is_retryable_status(408) is True
        assert is_retryable_status(429) is True
        assert is_retryable_status(500) is True
        assert is_retryable_status(502) is True
        assert is_retryable_status(503) is True
        assert is_retryable_status(504) is True

    def test_non_retryable_statuses(self) -> None:
        """Should identify non-retryable statuses."""
        assert is_retryable_status(400) is False
        assert is_retryable_status(401) is False
        assert is_retryable_status(403) is False
        assert is_retryable_status(404) is False


class TestMaskSensitive:
    """Tests for sensitive data masking."""

    def test_mask_long_string(self) -> None:
        """Should mask long strings."""
        result = mask_sensitive("lk_test_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        
        assert result.startswith("lk_test")
        assert result.endswith("aaaa")
        assert "****" in result

    def test_mask_short_string(self) -> None:
        """Should mask short strings completely."""
        result = mask_sensitive("short")
        
        assert result == "*****"


class TestValidateId:
    """Tests for ID validation."""

    def test_valid_user_id(self) -> None:
        """Should accept valid user ID."""
        validate_id("usr_abc123", "usr", "user ID")

    def test_valid_project_id(self) -> None:
        """Should accept valid project ID."""
        validate_id("prj_abc123", "prj", "project ID")

    def test_empty_id(self) -> None:
        """Should reject empty ID."""
        with pytest.raises(ValueError, match="user ID is required"):
            validate_id("", "usr", "user ID")

    def test_invalid_format(self) -> None:
        """Should reject invalid format."""
        with pytest.raises(ValueError, match="Invalid user ID format"):
            validate_id("invalid", "usr", "user ID")
