import pytest
from capture import Capture


def test_capture_initialization():
    client = Capture("test_key", "test_secret")
    assert client.key == "test_key"
    assert client.secret == "test_secret"
    assert client.options == {}


def test_capture_with_edge_option():
    client = Capture("test_key", "test_secret", {"useEdge": True})
    assert client.options.get("useEdge") is True


def test_build_image_url():
    client = Capture("test", "test")
    url = client.build_image_url("https://news.ycombinator.com/")
    expected_url = "https://cdn.capture.page/test/f37d5fb3ee4540a05bf4ffeed6dffa28/image?url=https%3A%2F%2Fnews.ycombinator.com%2F"
    assert url == expected_url


def test_build_image_url_with_options():
    client = Capture("test", "secret")
    url = client.build_image_url("https://news.ycombinator.com/", {"full": True, "delay": 2})
    assert "full=true" in url
    assert "delay=2" in url
    assert "url=https%3A%2F%2Fnews.ycombinator.com%2F" in url


def test_build_pdf_url():
    client = Capture("test", "secret")
    url = client.build_pdf_url("https://example.com")
    assert "/pdf?" in url
    assert "url=https%3A%2F%2Fexample.com" in url


def test_build_content_url():
    client = Capture("test", "secret")
    url = client.build_content_url("https://example.com")
    assert "/content?" in url
    assert "url=https%3A%2F%2Fexample.com" in url


def test_build_metadata_url():
    client = Capture("test", "secret")
    url = client.build_metadata_url("https://example.com")
    assert "/metadata?" in url
    assert "url=https%3A%2F%2Fexample.com" in url


def test_build_animated_url():
    client = Capture("test", "secret")
    url = client.build_animated_url("https://example.com")
    assert "/animated?" in url
    assert "url=https%3A%2F%2Fexample.com" in url


def test_edge_url_when_use_edge_enabled():
    client = Capture("test", "secret", {"useEdge": True})
    url = client.build_image_url("https://example.com")
    assert url.startswith("https://edge.capture.page")


def test_cdn_url_when_use_edge_disabled():
    client = Capture("test", "secret")
    url = client.build_image_url("https://example.com")
    assert url.startswith("https://cdn.capture.page")


def test_missing_key_raises_error():
    client = Capture("", "secret")
    with pytest.raises(ValueError, match="Key and Secret is required"):
        client.build_image_url("https://example.com")


def test_missing_secret_raises_error():
    client = Capture("test", "")
    with pytest.raises(ValueError, match="Key and Secret is required"):
        client.build_image_url("https://example.com")


def test_invalid_url_type_raises_error():
    client = Capture("test", "secret")
    with pytest.raises(TypeError, match="url should be of type string"):
        client.build_image_url(123)


def test_none_url_raises_error():
    client = Capture("test", "secret")
    with pytest.raises(ValueError, match="url is required"):
        client.build_image_url(None)


def test_filter_none_values():
    client = Capture("test", "test")
    url = client.build_image_url("https://example.com", {"none_value": None, "valid": "value"})
    assert "none_value=" not in url
    assert "valid=value" in url


def test_token_generation():
    client = Capture("test", "test")
    token = client._generate_token("test", "url=https%3A%2F%2Fnews.ycombinator.com%2F")
    assert token == "f37d5fb3ee4540a05bf4ffeed6dffa28"


def test_boolean_option_encoding():
    client = Capture("test", "secret")
    url = client.build_image_url("https://example.com", {"full": True, "lazy": False})
    assert "full=true" in url
    assert "lazy=false" in url


def test_numeric_option_encoding():
    client = Capture("test", "secret")
    url = client.build_image_url("https://example.com", {"delay": 5, "quality": 80})
    assert "delay=5" in url
    assert "quality=80" in url


def test_keep_zero_and_false_values():
    client = Capture("test", "test")
    url = client.build_image_url("https://example.com", {
        "delay": 0,
        "top": 0,
        "left": 0,
        "full": False,
        "darkMode": False
    })
    assert "delay=0" in url
    assert "top=0" in url
    assert "left=0" in url
    assert "full=false" in url
    assert "darkMode=false" in url


@pytest.mark.asyncio
async def test_fetch_image():
    client = Capture("test", "secret")
    url = client.build_image_url("https://example.com")
    assert url is not None


@pytest.mark.asyncio
async def test_fetch_pdf():
    client = Capture("test", "secret")
    url = client.build_pdf_url("https://example.com")
    assert url is not None


@pytest.mark.asyncio
async def test_fetch_content():
    client = Capture("test", "secret")
    url = client.build_content_url("https://example.com")
    assert url is not None


@pytest.mark.asyncio
async def test_fetch_metadata():
    client = Capture("test", "secret")
    url = client.build_metadata_url("https://example.com")
    assert url is not None


@pytest.mark.asyncio
async def test_fetch_animated():
    client = Capture("test", "secret")
    url = client.build_animated_url("https://example.com")
    assert url is not None
