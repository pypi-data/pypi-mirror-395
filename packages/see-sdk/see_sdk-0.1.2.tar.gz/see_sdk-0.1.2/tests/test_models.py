"""Tests for data models."""

import pytest

from see.models import (
    CreateShortUrlRequest,
    CreateShortUrlResponse,
    UpdateShortUrlRequest,
    UpdateShortUrlResponse,
    DeleteShortUrlRequest,
    DeleteShortUrlResponse,
    DomainResponse,
    Tag,
    TagResponse,
)


def test_create_short_url_request_from_dict() -> None:
    """Test creating CreateShortUrlRequest from dictionary."""
    data = {
        "domain": "example.com",
        "target_url": "https://example.com/long/url",
        "expiration_redirect_url": "https://example.com/expired",
        "expire_at": 1735689599,
        "password": "secret123",
        "title": "Test Link",
        "custom_slug": "my-link",
        "tag_ids": [1, 2, 3],
    }

    request = CreateShortUrlRequest.from_dict(data)

    assert request.domain == "example.com"
    assert request.target_url == "https://example.com/long/url"
    assert request.expiration_redirect_url == "https://example.com/expired"
    assert request.expire_at == 1735689599
    assert request.password == "secret123"
    assert request.title == "Test Link"
    assert request.custom_slug == "my-link"
    assert request.tag_ids == [1, 2, 3]


def test_create_short_url_request_minimal() -> None:
    """Test creating CreateShortUrlRequest with minimal fields."""
    data = {
        "domain": "example.com",
        "target_url": "https://example.com/target",
    }

    request = CreateShortUrlRequest.from_dict(data)

    assert request.domain == "example.com"
    assert request.target_url == "https://example.com/target"
    assert request.expiration_redirect_url == ""
    assert request.expire_at == 0
    assert request.password == ""
    assert request.title == ""
    assert request.custom_slug == ""
    assert request.tag_ids == []


def test_create_short_url_response_from_dict() -> None:
    """Test creating CreateShortUrlResponse from dictionary."""
    data = {
        "code": 0,
        "data": {
            "short_url": "https://example.com/abc123",
            "slug": "abc123",
        },
        "message": "Success",
    }

    response = CreateShortUrlResponse.from_dict(data)

    assert response.code == 0
    assert response.data == {"short_url": "https://example.com/abc123", "slug": "abc123"}
    assert response.message == "Success"


def test_update_short_url_request_from_dict() -> None:
    """Test creating UpdateShortUrlRequest from dictionary."""
    data = {
        "domain": "example.com",
        "slug": "abc123",
        "target_url": "https://example.com/new-target",
        "title": "Updated Title",
    }

    request = UpdateShortUrlRequest.from_dict(data)

    assert request.domain == "example.com"
    assert request.slug == "abc123"
    assert request.target_url == "https://example.com/new-target"
    assert request.title == "Updated Title"


def test_update_short_url_response_from_dict() -> None:
    """Test creating UpdateShortUrlResponse from dictionary."""
    data = {
        "code": 0,
        "data": None,
        "message": "Updated successfully",
    }

    response = UpdateShortUrlResponse.from_dict(data)

    assert response.code == 0
    assert response.message == "Updated successfully"


def test_delete_short_url_request_from_dict() -> None:
    """Test creating DeleteShortUrlRequest from dictionary."""
    data = {
        "domain": "example.com",
        "slug": "abc123",
    }

    request = DeleteShortUrlRequest.from_dict(data)

    assert request.domain == "example.com"
    assert request.slug == "abc123"


def test_delete_short_url_response_from_dict() -> None:
    """Test creating DeleteShortUrlResponse from dictionary."""
    data = {
        "code": 0,
        "data": None,
        "message": "Deleted successfully",
    }

    response = DeleteShortUrlResponse.from_dict(data)

    assert response.code == 0
    assert response.message == "Deleted successfully"


def test_domain_response_from_dict() -> None:
    """Test creating DomainResponse from dictionary."""
    data = {
        "code": 0,
        "data": {
            "domains": ["example.com", "short.link", "my.link"]
        },
        "message": "Success",
    }

    response = DomainResponse.from_dict(data)

    assert response.code == 0
    assert response.data == {"domains": ["example.com", "short.link", "my.link"]}
    assert response.message == "Success"


def test_tag_from_dict() -> None:
    """Test creating Tag from dictionary."""
    data = {
        "id": 123,
        "name": "Marketing",
    }

    tag = Tag.from_dict(data)

    assert tag.id == 123
    assert tag.name == "Marketing"


def test_tag_response_from_dict() -> None:
    """Test creating TagResponse from dictionary."""
    data = {
        "code": 0,
        "data": {
            "tags": [
                {"id": 1, "name": "Marketing"},
                {"id": 2, "name": "Sales"},
                {"id": 3, "name": "Support"},
            ]
        },
        "message": "Success",
    }

    response = TagResponse.from_dict(data)

    assert response.code == 0
    assert response.data == {
        "tags": [
            {"id": 1, "name": "Marketing"},
            {"id": 2, "name": "Sales"},
            {"id": 3, "name": "Support"},
        ]
    }
    assert response.message == "Success"


def test_create_short_url_request_immutable() -> None:
    """Test that CreateShortUrlRequest is immutable (frozen dataclass)."""
    request = CreateShortUrlRequest(
        domain="example.com",
        target_url="https://example.com/target",
    )

    with pytest.raises(AttributeError):
        request.domain = "other.com"  # type: ignore


def test_tag_immutable() -> None:
    """Test that Tag is immutable (frozen dataclass)."""
    tag = Tag(id=1, name="Test")

    with pytest.raises(AttributeError):
        tag.name = "Updated"  # type: ignore
