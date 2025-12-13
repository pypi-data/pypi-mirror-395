# Development Guidelines for biosites

## Code Style and Best Practices

### Python Typing (PEP 585 - Python 3.9+)

Use modern Python typing syntax for all type annotations:

#### ✅ DO Use
```python
# Modern union syntax for optional types
def process(url: str, proxy: str | None = None) -> dict[str, Any]:
    pass

# Built-in generic types
def get_links() -> list[ExtractedLink]:
    pass

def get_metadata() -> dict[str, str]:
    pass

# Multiple union types
def parse_data(data: str | bytes | None) -> list[str]:
    pass
```

#### ❌ DON'T Use
```python
# Old Optional syntax
from typing import Optional, List, Dict
def process(url: str, proxy: Optional[str] = None) -> Dict[str, Any]:
    pass

# Old generic types from typing module
def get_links() -> List[ExtractedLink]:
    pass

def get_metadata() -> Dict[str, str]:
    pass
```

### Import Guidelines

#### Standard Type Hints
- Use built-in types directly: `list`, `dict`, `set`, `tuple`
- Use union syntax: `X | Y` instead of `Union[X, Y]`
- Use `X | None` instead of `Optional[X]`

#### When to Import from `typing`
Only import from `typing` when you need:
- `Any`
- `TypeVar`, `Generic`
- `Protocol`, `TypedDict`
- `Literal`, `Final`
- `cast`, `overload`

### Code Formatting

Use **Ruff** for all code formatting and linting:
```bash
ruff check biosites/
ruff format biosites/
```

**Do NOT use Black formatter** - Ruff is the single formatter for this project.

### Async Best Practices

1. All I/O operations should be async
2. Use `aiohttp` for HTTP requests
3. Support session reuse for efficiency
4. Always handle proxy configuration

### Error Handling

1. Gracefully handle extraction failures
2. Return empty results with error messages rather than raising exceptions
3. Log errors in the `errors` field of `ExtractionResult`

### Testing

1. Use pytest with pytest-asyncio for async tests
2. Store HTML fixtures in `tests/fixtures/`
3. Mock network calls in tests
4. Test both success and failure cases

### Proxy Support

Always support proxy configuration:
- Accept proxy parameter in constructors
- Accept proxy parameter in async methods
- CLI should respect `HTTP_PROXY` and `http_proxy` environment variables
- CLI `--proxy` flag takes precedence over environment variables

## Architecture

### Class Hierarchy

```
BaseLinkExtractor (ABC)
├── GenericLinkExtractor (fallback for any URL)
└── [Service]Extractor (specific implementations)
    └── LittlyExtractor
    └── LinktreeExtractor (future)
    └── ...
```

### Adding New Extractors - Step by Step Guide

Based on our implementation experience with Linktree, Litt.ly, InPock, and lit.link extractors, here's the recommended workflow:

#### 1. Research & Analysis Phase

**Fetch and save the target page:**
```bash
curl -s "https://example-service.com/username" \
  -H "User-Agent: Mozilla/5.0" \
  -o tests/fixtures/servicename_username.html
```

**Analyze the page structure:**
```python
# Check for common patterns
from selectolax.parser import HTMLParser
import re

with open('tests/fixtures/servicename_username.html', 'r') as f:
    html = f.read()

# Look for JSON data structures
patterns = ['window.__NEXT_DATA__', 'window.__NUXT__', 'script#data', 'profileLinks']
for pattern in patterns:
    if pattern in html:
        print(f'Found pattern: {pattern}')

# Check for base64 encoded data
import re
script_tags = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for script in script_tags:
    if len(script) > 1000 and '=' in script:  # Might be base64
        print('Potential base64 data found')

# Count links in regular HTML
parser = HTMLParser(html)
links = parser.css('a[href]')
print(f'Found {len(links)} <a> tags')
```

#### 2. Identify Data Sources

Services typically store link data in one or more of these locations:

**a) JSON in script tags:**
- **Linktree**: `script#__NEXT_DATA__` with JSON
- **InPock**: `window.__NUXT__` with complex nested data
- **lit.link**: JSON objects in script tags

**b) Base64 encoded data:**
- **Litt.ly**: `script#data` with base64-encoded JSON

**c) Server-side rendered HTML:**
- **InPock**: Links in `div.interaction-block-wrapper`
- **lit.link (fallback)**: Regular `<a>` tags

**d) Mixed approach:**
- **InPock**: Combines SSR links with NUXT social data

#### 3. Implementation Pattern

Create `biosites/extractors/servicename.py`:

```python
import json
import re
from urllib.parse import urlparse
from pydantic import HttpUrl
from selectolax.parser import HTMLParser

from ..base import BaseLinkExtractor
from ..models import ExtractedLink


class ServiceNameExtractor(BaseLinkExtractor):
    def can_handle(self, url: str) -> bool:
        return "servicename.com" in url
    
    async def extract_links(self, html: str, url: str) -> list[ExtractedLink]:
        links: list[ExtractedLink] = []
        
        # Try primary extraction method
        links.extend(self._extract_primary_method(html))
        
        # Try secondary/fallback methods if needed
        if not links:
            links.extend(self._extract_fallback_method(html))
        
        # Filter out service's own URLs
        links = self._filter_service_urls(links)
        
        # Deduplicate
        return self._deduplicate_links(links)
    
    def _extract_primary_method(self, html: str) -> list[ExtractedLink]:
        """Primary extraction logic"""
        links = []
        # Your extraction logic here
        return links
    
    def _filter_service_urls(self, links: list[ExtractedLink]) -> list[ExtractedLink]:
        """Remove service's internal URLs"""
        filtered = []
        for link in links:
            # Skip service's own domains
            if not self._is_service_url(str(link.url)):
                filtered.append(link)
        return filtered
    
    def _is_service_url(self, url: str) -> bool:
        """Check if URL belongs to the service itself"""
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            return 'servicename.com' in hostname
        except:
            return 'servicename.com' in url
    
    def _deduplicate_links(self, links: list[ExtractedLink]) -> list[ExtractedLink]:
        """Remove duplicate URLs, keeping the one with more metadata"""
        seen = {}
        for link in links:
            url_str = str(link.url)
            if url_str not in seen:
                seen[url_str] = link
            else:
                # Keep the one with more info
                existing = seen[url_str]
                if not existing.title and link.title:
                    seen[url_str] = link
        return list(seen.values())
```

#### 4. Common Extraction Patterns

**For JSON data:**
```python
# Find and parse JSON
match = re.search(r'window\.__DATA__=(.*?);</script>', html, re.DOTALL)
if match:
    try:
        data = json.loads(match.group(1))
        # Extract from data structure
    except json.JSONDecodeError:
        pass
```

**For base64 data:**
```python
import pybase64

script = parser.css_first('script#data')
if script:
    base64_content = script.text().strip()
    decoded = pybase64.b64decode(base64_content).decode('utf-8')
    data = json.loads(decoded)
```

**For HTML links:**
```python
parser = HTMLParser(html)
for link in parser.css('a[href]'):
    href = link.attributes.get('href', '') or ''
    href = href.strip()
    if href.startswith(('http://', 'https://')):
        # Process link
```

#### 5. Handle Edge Cases

1. **Unicode escapes in URLs:**
```python
url = url.encode().decode('unicode_escape')
```

2. **Relative URLs:**
```python
if href.startswith('//'):
    href = f'https:{href}'
elif href.startswith('/'):
    parsed = urlparse(base_url)
    href = f'{parsed.scheme}://{parsed.netloc}{href}'
```

3. **Multiple data sources (like InPock):**
```python
# Combine from multiple sources
links.extend(self._extract_ssr_links(html))
links.extend(self._extract_json_links(html))
# Then deduplicate
```

#### 6. Testing Strategy

Create `tests/test_servicename.py`:

```python
import pytest
from pathlib import Path
from biosites.extractors.servicename import ServiceNameExtractor

@pytest.fixture
def service_html():
    fixture_path = Path(__file__).parent / "fixtures" / "servicename_username.html"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.mark.asyncio
async def test_servicename_extract_links(service_html):
    extractor = ServiceNameExtractor()
    links = await extractor.extract_links(service_html, "https://servicename.com/user")
    
    # Test link count
    assert len(links) > 0
    
    # Test for expected URLs
    extracted_urls = [str(link.url) for link in links]
    assert "https://expected-url.com" in extracted_urls
    
    # Verify no service URLs included
    for url in extracted_urls:
        assert 'servicename.com' not in url
```

#### 7. Registration

Update `biosites/extractors/__init__.py`:
```python
from .servicename import ServiceNameExtractor
__all__ = [..., "ServiceNameExtractor"]
```

Update `biosites/extractor.py`:
```python
from .extractors import ..., ServiceNameExtractor

def _register_extractors(self) -> None:
    # ...
    self.register_extractor(ServiceNameExtractor(self.session, self.proxy))
```

#### 8. Validation Checklist

- [ ] Run tests: `pytest tests/test_servicename.py -v`
- [ ] Check linting: `ruff check biosites/`
- [ ] **Check types with pyright: `pyright biosites tests`**
- [ ] Check types with mypy: `mypy biosites/`  
- [ ] Test CLI: `biosites https://servicename.com/user`
- [ ] Test JSON output: `biosites https://servicename.com/user -o json`
- [ ] Verify proxy support works
- [ ] Ensure service's own URLs are excluded
- [ ] Handle edge cases (empty data, malformed HTML, etc.)

## Type Checking Requirements

### Pyright Configuration
The project uses **pyright** for strict type checking. Configuration is in `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "strict"
```

### Pre-commit Type Checking
**ALWAYS run pyright before committing:**
```bash
pyright biosites tests
```

### Common Pyright Issues to Fix:
1. **Optional member access**: Always check for None before accessing attributes
   ```python
   # ❌ Bad
   if "instagram" in link.title.lower():
   
   # ✅ Good  
   if link.title and "instagram" in link.title.lower():
   ```

2. **Missing type annotations**: Add types to all function parameters
   ```python
   # ❌ Bad
   def process_data(data):
   
   # ✅ Good
   def process_data(data: dict[str, Any]):
   ```

3. **Protected member access**: Don't use `_` prefixed members outside their class
   ```python
   # ❌ Bad
   extractor._internal_method()
   
   # ✅ Good
   extractor.public_method()
   ```

## CLI Design

### Output Formats
- **CLI mode**: Human-readable with colors and formatting
- **JSON mode**: Machine-readable for scripting

### Verbosity Levels
- Default: Concise output
- Verbose (`-v`): Full URLs and metadata

## Dependencies

Core dependencies (keep minimal):
- `selectolax`: HTML parsing
- `pybase64`: Base64 operations
- `aiohttp`: Async HTTP
- `pydantic`: Data validation

Dev dependencies:
- `ruff`: Linting and formatting
- `mypy`: Type checking
- `pytest` + `pytest-asyncio`: Testing