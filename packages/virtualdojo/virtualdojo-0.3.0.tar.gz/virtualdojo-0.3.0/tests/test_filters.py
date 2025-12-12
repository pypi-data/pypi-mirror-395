"""Tests for filter parsing utilities."""

import json

import pytest

from virtualdojo.utils.filters import parse_filters


def test_simple_equality():
    """Test simple key=value filter."""
    result = parse_filters("status=active")
    data = json.loads(result)
    assert data == {"status": "active"}


def test_multiple_filters():
    """Test multiple comma-separated filters."""
    result = parse_filters("status=active,tier=enterprise")
    data = json.loads(result)
    assert data == {"status": "active", "tier": "enterprise"}


def test_operator_filter():
    """Test filter with operator suffix."""
    result = parse_filters("amount_gte=10000")
    data = json.loads(result)
    assert data == {"amount_gte": 10000}


def test_multiple_operators():
    """Test multiple operator filters."""
    result = parse_filters("amount_gte=10000,stage_ne=closed,name_contains=Acme")
    data = json.loads(result)
    assert data == {
        "amount_gte": 10000,
        "stage_ne": "closed",
        "name_contains": "Acme",
    }


def test_boolean_values():
    """Test boolean value parsing."""
    result = parse_filters("is_active=true,is_deleted=false")
    data = json.loads(result)
    assert data == {"is_active": True, "is_deleted": False}


def test_null_values():
    """Test null value parsing."""
    result = parse_filters("email_isnull=true,phone=null")
    data = json.loads(result)
    assert data == {"email_isnull": True, "phone": None}


def test_numeric_values():
    """Test numeric value parsing."""
    result = parse_filters("count=42,price=19.99")
    data = json.loads(result)
    assert data == {"count": 42, "price": 19.99}


def test_quoted_values():
    """Test quoted value handling."""
    result = parse_filters('name="John Doe",city=\'New York\'')
    data = json.loads(result)
    assert data == {"name": "John Doe", "city": "New York"}


def test_json_passthrough():
    """Test that valid JSON is passed through."""
    json_filter = '{"field": "value", "amount_gte": 100}'
    result = parse_filters(json_filter)
    assert result == json_filter


def test_empty_filter():
    """Test empty filter string."""
    result = parse_filters("")
    data = json.loads(result)
    assert data == {}
