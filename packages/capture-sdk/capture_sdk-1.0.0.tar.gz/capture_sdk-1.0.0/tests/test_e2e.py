import os

import pytest

from capture import Capture

CAPTURE_API_KEY = os.environ.get("CAPTURE_API_KEY")
CAPTURE_API_SECRET = os.environ.get("CAPTURE_API_SECRET")
TEST_URL = "https://techulus.xyz"

skip_if_no_credentials = pytest.mark.skipif(
    not CAPTURE_API_KEY or not CAPTURE_API_SECRET,
    reason="E2E tests require CAPTURE_API_KEY and CAPTURE_API_SECRET environment variables"
)

@pytest.fixture
def client():
    return Capture(CAPTURE_API_KEY, CAPTURE_API_SECRET)

@pytest.fixture
def edge_client():
    return Capture(CAPTURE_API_KEY, CAPTURE_API_SECRET, {"useEdge": True})

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_fetch_image_successfully(client):
    image_data = await client.fetch_image(TEST_URL)
    assert isinstance(image_data, bytes)
    assert len(image_data) > 0

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_fetch_pdf_successfully(client):
    pdf_data = await client.fetch_pdf(TEST_URL)
    assert isinstance(pdf_data, bytes)
    assert len(pdf_data) > 0

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_fetch_content_successfully(client):
    content = await client.fetch_content(TEST_URL)
    assert content["success"] is True
    assert "html" in content
    assert "textContent" in content
    assert len(content["html"]) > 0

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_fetch_metadata_successfully(client):
    metadata = await client.fetch_metadata(TEST_URL)
    assert metadata["success"] is True
    assert "metadata" in metadata
    assert len(metadata["metadata"]) > 0

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_fetch_animated_successfully(client):
    animated_data = await client.fetch_animated(TEST_URL)
    assert isinstance(animated_data, bytes)
    assert len(animated_data) > 0

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_fetch_image_with_options(client):
    image_data = await client.fetch_image(TEST_URL, {"full": True, "delay": 2})
    assert isinstance(image_data, bytes)
    assert len(image_data) > 0

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_edge_url_fetches_successfully(edge_client):
    image_data = await edge_client.fetch_image(TEST_URL)
    assert isinstance(image_data, bytes)
    assert len(image_data) > 0

@skip_if_no_credentials
@pytest.mark.asyncio
async def test_all_fetch_methods_together(client):
    image_data = await client.fetch_image(TEST_URL)
    assert len(image_data) > 0

    pdf_data = await client.fetch_pdf(TEST_URL)
    assert len(pdf_data) > 0

    content = await client.fetch_content(TEST_URL)
    assert content["success"] is True
    assert len(content["html"]) > 0

    metadata = await client.fetch_metadata(TEST_URL)
    assert metadata["success"] is True
    assert metadata["metadata"]
