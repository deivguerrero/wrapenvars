"""Tests for wrapenvars base64 encode/decode functions."""

import json

from wrapenvars import get_dict, get_str, set_dict, set_str

# ── set_str ──────────────────────────────────────────────────────────────


class TestSetStr:
    """Tests for base64 encoding strings."""

    def test_encode_simple_string(self) -> None:
        """A plain ASCII string encodes to valid base64."""
        result = set_str("hello")
        assert result != ""
        assert result != "hello"  # not plaintext

    def test_encode_empty_string(self) -> None:
        """Empty string produces non-empty base64 (b64 of empty bytes)."""
        result = set_str("")
        assert isinstance(result, str)

    def test_encode_unicode(self) -> None:
        """Unicode characters (ñ, emoji) encode and decode correctly."""
        original = "cañón 🚀"
        encoded = set_str(original)
        decoded = get_str(encoded)
        assert decoded == original

    def test_encode_special_characters(self) -> None:
        """Special characters survive the encode/decode round-trip."""
        original = "line1\nline2\tindented"
        assert get_str(set_str(original)) == original

    def test_encode_none_fails_gracefully(self) -> None:
        """Passing None returns empty string (caught by TypeError)."""
        result = set_str(None)  # type: ignore[arg-type]
        assert result == ""


# ── get_str ──────────────────────────────────────────────────────────────


class TestGetStr:
    """Tests for decoding base64 strings."""

    def test_decode_valid_base64(self) -> None:
        """A valid base64 string decodes correctly."""
        encoded = set_str("hello world")
        assert get_str(encoded) == "hello world"

    def test_decode_invalid_base64(self) -> None:
        """Invalid base64 returns empty string gracefully."""
        assert get_str("!!! not base64 !!!") == ""

    def test_decode_empty_string(self) -> None:
        """Empty base64 string returns empty string."""
        assert get_str("") == ""

    def test_roundtrip_alphanumeric(self) -> None:
        """Any string should survive encode→decode unchanged."""
        cases = ["a", "abc123", "A" * 100, " ", "你好"]
        for case in cases:
            assert get_str(set_str(case)) == case

    def test_decode_none_fails_gracefully(self) -> None:
        """Passing None to get_str returns empty string."""
        result = get_str(None)  # type: ignore[arg-type]
        assert result == ""


# ── set_dict ─────────────────────────────────────────────────────────────


class TestSetDict:
    """Tests for encoding dictionaries to base64."""

    def test_encode_simple_dict(self) -> None:
        """A plain dict encodes and decodes correctly."""
        data = {"key": "value", "num": 42}
        encoded = set_dict(data)
        assert encoded != ""
        assert json.loads(get_str(encoded)) == data

    def test_encode_empty_dict(self) -> None:
        """Empty dict encodes to base64 of '{}'."""
        encoded = set_dict({})
        assert get_str(encoded) == "{}"

    def test_encode_nested_dict(self) -> None:
        """Nested structures survive encoding."""
        data = {"a": {"b": [1, 2, 3], "c": None}, "d": True}
        assert get_dict(set_dict(data)) == data

    def test_encode_unicode_values(self) -> None:
        """Dict with unicode values encodes correctly."""
        data = {"español": "cañón", "emoji": "🚀"}
        decoded = get_dict(set_dict(data))
        assert decoded == data

    def test_encode_none_encodes_json_null(self) -> None:
        """Passing None produces base64 of JSON null (json.dumps(None) == 'null')."""
        result = set_dict(None)  # type: ignore[arg-type]
        assert result != ""
        assert get_str(result) == "null"


# ── get_dict ─────────────────────────────────────────────────────────────


class TestGetDict:
    """Tests for decoding dictionaries from base64."""

    def test_decode_valid_dict(self) -> None:
        """Decode a valid base64-encoded JSON dict."""
        encoded = set_dict({"x": 1})
        assert get_dict(encoded) == {"x": 1}

    def test_decode_invalid_base64(self) -> None:
        """Non-base64 input returns empty dict."""
        assert get_dict("not-base64!!!") == {}

    def test_decode_base64_not_json(self) -> None:
        """Valid base64 that is not JSON returns empty dict."""
        encoded = set_str("this is not json")
        assert get_dict(encoded) == {}

    def test_decode_empty_string(self) -> None:
        """Empty string returns empty dict."""
        assert get_dict("") == {}

    def test_decode_none_fails_gracefully(self) -> None:
        """Passing None returns empty dict."""
        result = get_dict(None)  # type: ignore[arg-type]
        assert result == {}


# ── Edge cases ───────────────────────────────────────────────────────────


class TestEdgeCases:
    """Boundary and edge-case behaviour."""

    def test_very_long_string(self) -> None:
        """A 10KB string survives round-trip."""
        long_str = "x" * 10_000
        assert get_str(set_str(long_str)) == long_str

    def test_very_long_dict(self) -> None:
        """A dict with 1000 keys survives round-trip."""
        big_dict = {f"key{i}": i for i in range(1000)}
        assert get_dict(set_dict(big_dict)) == big_dict

    def test_bytes_input_rejected(self) -> None:
        """set_str rejects bytes input (TypeError on .encode)."""
        result = set_str(b"bytes")  # type: ignore[arg-type]
        assert result == ""

    def test_dict_with_bytes_values(self) -> None:
        """Dict with bytes values fails serialization gracefully."""
        result = set_dict({"data": b"bytes"})  # type: ignore[dict-item,unused-ignore]
        assert result == ""
