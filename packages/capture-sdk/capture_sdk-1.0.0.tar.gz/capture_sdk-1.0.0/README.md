# Capture Python SDK

Official Python SDK for [Capture](https://capture.page) - Screenshot and content extraction API.

## Installation

```bash
pip install capture-sdk
```

## Quick Start

```python
from capture import Capture

client = Capture("your-api-key", "your-api-secret")

image_url = client.build_image_url("https://example.com")
print(image_url)
```

## Features

- **Screenshot Capture**: Capture full-page or viewport screenshots as PNG/JPG
- **PDF Generation**: Convert web pages to PDF documents
- **Content Extraction**: Extract HTML and text content from web pages
- **Metadata Extraction**: Get page metadata (title, description, og tags, etc.)
- **Animated GIFs**: Create animated GIFs of page interactions
- **Async Support**: Built-in async/await support for all fetch methods
- **Type Hints**: Full type hint support for better IDE integration

## Usage

### Initialize the Client

```python
from capture import Capture

client = Capture("your-api-key", "your-api-secret")

client_with_edge = Capture("your-api-key", "your-api-secret", {"useEdge": True})
```

### Building URLs

The SDK provides URL builders for each capture type:

#### Image Capture

```python
image_url = client.build_image_url("https://example.com")

image_url_with_options = client.build_image_url(
    "https://example.com",
    {
        "full": True,
        "delay": 2,
        "width": 1920,
        "height": 1080,
        "quality": 90
    }
)
```

#### PDF Capture

```python
pdf_url = client.build_pdf_url("https://example.com")

pdf_url_with_options = client.build_pdf_url(
    "https://example.com",
    {
        "full": True,
        "delay": 1
    }
)
```

#### Content Extraction

```python
content_url = client.build_content_url("https://example.com")
```

#### Metadata Extraction

```python
metadata_url = client.build_metadata_url("https://example.com")
```

#### Animated GIF

```python
animated_url = client.build_animated_url("https://example.com")
```

### Fetching Data (Async)

The SDK provides async methods to fetch data directly:

#### Fetch Image

```python
import asyncio

async def main():
    image_data = await client.fetch_image("https://example.com")
    with open("screenshot.png", "wb") as f:
        f.write(image_data)

asyncio.run(main())
```

#### Fetch PDF

```python
async def main():
    pdf_data = await client.fetch_pdf("https://example.com", {"full": True})
    with open("page.pdf", "wb") as f:
        f.write(pdf_data)

asyncio.run(main())
```

#### Fetch Content

```python
async def main():
    content = await client.fetch_content("https://example.com")
    print(content["html"])
    print(content["textContent"])

asyncio.run(main())
```

#### Fetch Metadata

```python
async def main():
    metadata = await client.fetch_metadata("https://example.com")
    print(metadata["metadata"])

asyncio.run(main())
```

#### Fetch Animated GIF

```python
async def main():
    gif_data = await client.fetch_animated("https://example.com")
    with open("animation.gif", "wb") as f:
        f.write(gif_data)

asyncio.run(main())
```

## Configuration Options

### Constructor Options

- `useEdge` (bool): Use edge.capture.page instead of cdn.capture.page for faster response times

## API Endpoints

The SDK supports two base URLs:

- **CDN**: `https://cdn.capture.page` (default)
- **Edge**: `https://edge.capture.page` (when `useEdge: True`)

## Type Hints

The SDK includes full type hint support:

```python
from capture import Capture, RequestOptions

options: RequestOptions = {
    "full": True,
    "delay": 2,
    "width": 1920
}

client = Capture("key", "secret")
url: str = client.build_image_url("https://example.com", options)
```

## License

MIT

## Links

- [Website](https://capture.page)
- [Documentation](https://docs.capture.page)
- [API Reference](https://docs.capture.page/api)
- [GitHub](https://github.com/techulus/capture-py)

## Support

For support, please visit [capture.page](https://capture.page) or open an issue on GitHub.
