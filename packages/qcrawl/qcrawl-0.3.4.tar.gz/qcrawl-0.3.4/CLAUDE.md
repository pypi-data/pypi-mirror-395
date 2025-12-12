# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

qCrawl is a fast async web crawling & scraping framework for Python that extracts structured data from web pages. It's similar to Scrapy but built on asyncio with a focus on high throughput and extensibility through middleware.

**Key Technologies:**
- **asyncio** for concurrency
- **aiohttp** for HTTP client
- **lxml** for HTML parsing
- **msgspec** for fast request serialization in scheduler queues
- **orjson** for high-performance JSON operations

## Naming Conventions and Branding

Never use "Scrapy" terminology in qCrawl code**

- ❌ **NEVER** use "scrapy" in variable names, function names, settings, or documentation
- ❌ **NEVER** use settings like "use_scrapy_headers" or similar Scrapy-inspired names
- ✅ **ALWAYS** use "qcrawl" branding: "use_qcrawl_headers", "qCrawl headers", etc.
- ✅ **ALWAYS** refer to the framework as "qCrawl" (not Scrapy) in code and docs

While qCrawl is inspired by Scrapy's architecture, it is a distinct framework with its own identity. All naming should reflect the qCrawl brand consistently across:
- Settings names (e.g., `CAMOUFOX_PROCESS_REQUEST_HEADERS = "use_qcrawl_headers"`)
- Variable names
- Function names
- Documentation
- Comments
- Test names

## Development Commands

**Linting and Type Checking:**
```bash
ruff check .           # Run linter
mypy .                 # Run type checker
```

**Testing:**
```bash
pytest                 # Run all tests
pytest -m "not integration"  # Run unit tests only (fast)
pytest -m integration  # Run integration tests only (requires Docker)
pytest tests/path/to/test_file.py::test_function  # Run single test
pytest --cov=qcrawl --cov-report=term-missing     # Run with coverage
```

## Testing Approach

**Philosophy:**
- Quality over quantity: Focus on high-value integration tests over exhaustive unit tests
- Test behavior, not implementation: Avoid testing private methods or internal details
- Follow pytest best practices: Use functions with fixtures, not test classes

**Test Structure:**
- **Shared fixtures**: Use `tests/conftest.py` for project-wide fixtures (e.g., `dummy_spider`, `run_coro_sync`)
- **Module-specific fixtures**: Use `tests/*/conftest.py` for module-specific fixtures
- **Clear organization**: Use section comments (`# Initialization Tests`, `# Settings Tests`, etc.)
- **Descriptive names**: Test names should clearly describe what they test (e.g., `test_spider_init_valid`)

**Best Practices:**
- ✅ Use pytest fixtures instead of class-based setup/teardown
- ✅ Use `@pytest.mark.parametrize` for testing multiple scenarios
- ✅ Follow AAA pattern: Arrange, Act, Assert
- ✅ Test public API only, not private methods
- ✅ Use `tmp_path` fixture for file operations
- ✅ Use `monkeypatch` for environment variables and sys.argv
- ❌ Don't create test classes unless they share state (rare)
- ❌ Don't test implementation details
- ❌ Don't duplicate test helpers - use fixtures

**Challenge Inconsistent Behavior:**
- When tests reveal inconsistent behavior in implementation, **fix the implementation** rather than testing around it
- Example: If a function returns different formats in different cases (e.g., empty vs non-empty), standardize the implementation
- Tests should verify correct, consistent behavior - not accommodate bugs or inconsistencies
- Ask: "Is this the right behavior?" before writing tests that work around implementation quirks

**Mocking Strategy (Mock at Boundaries):**
- ✅ DO mock: `aiohttp.ClientSession`, `Redis`, external APIs, `datetime.now()`, `sys.argv`
  - Reason: Fast, deterministic tests; control edge cases (timeouts, errors)
- ❌ DON'T mock: `Spider`, `Crawler`, `Engine`, `Request`, `Item`, internal methods
  - Reason: Catch real integration bugs; tests survive refactoring
- Rule: Mock what you don't control (external), test what you do control (your code)

**Integration Tests with Docker (Preferred):**
- Use `testcontainers` for integration tests instead of mocking HTTP
- Tests in `tests/integration/` marked with `@pytest.mark.integration`
- Test against REAL services: httpbin for HTTP, Redis for queue backend
- Example: `httpbin_server` fixture provides real HTTP server in Docker
- NO mocking of internal qCrawl components - test actual behavior
- See `docs/extending/testing.md` for complete guide

**Example Test Pattern:**
```python
# tests/conftest.py - Shared fixtures
@pytest.fixture
def dummy_spider():
    """Provide a DummySpider instance."""
    return DummySpider()

# tests/core/test_example.py - Organized tests
# Initialization Tests

def test_component_init_valid(dummy_spider):
    """Component initializes with valid parameters."""
    component = Component(dummy_spider)

    assert component.spider is dummy_spider
    assert component.state == "initialized"

# Error Handling Tests

@pytest.mark.parametrize("invalid_input", [None, "", []])
def test_component_rejects_invalid_input(invalid_input):
    """Component raises TypeError for invalid input."""
    with pytest.raises(TypeError, match="must be non-empty"):
        Component(invalid_input)
```

**Running Examples:**
```bash
python example_cli.py              # CLI-based spider example
python example_programmable.py     # Programmatic spider example
qcrawl run example_cli.py          # Using qcrawl CLI
```

## Architecture

### Core Components (Request Flow)

The architecture follows a pipeline pattern with middleware:

```
Spider.start_requests()
    ↓
[Spider Middlewares] (start_requests phase)
    ↓
Scheduler (priority queue + fingerprinting for deduplication)
    ↓
[Downloader Middlewares] (process_request)
    ↓
Downloader (aiohttp HTTP fetch)
    ↓
[Downloader Middlewares] (process_response/process_exception)
    ↓
[Spider Middlewares] (input phase)
    ↓
Spider.parse(response) → yields Items/Requests
    ↓
[Spider Middlewares] (output phase)
    ↓
Pipelines (for Items) OR back to Scheduler (for Requests)
```

### Key Classes

**Crawler** (`qcrawl/core/crawler.py`):
- High-level API accepting a Spider and Settings
- Manages component lifecycle (create Downloader, Scheduler, Engine)
- Handles middleware registration and resolution
- Registers signal handlers for stats collection
- Settings precedence: base Settings → spider.custom_settings → CLI args

**CrawlEngine** (`qcrawl/core/engine.py`):
- Core orchestrator for scheduler/downloader/spider
- Executes downloader middleware chains
- Manages worker tasks for concurrent request processing
- Signal emission for observability

**Settings** (`qcrawl/settings.py`):
- Frozen dataclass with UPPERCASE field names
- Immutable with `with_overrides()` method for creating new instances
- Priority system via `Priority` enum (DEFAULT < CONFIG_FILE < ENV < SPIDER < CLI < EXPLICIT)
- All settings keys are UPPERCASE; `get_setting()` performs case-insensitive lookup

**Spider** (`qcrawl/core/spider.py`):
- Base class for spiders
- `start_requests()` yields initial Requests
- `parse(response)` yields Items or more Requests
- Can define `custom_settings` dict to override Settings

**Item** (`qcrawl/core/item.py`):
- Flexible data container with `dict[str, object]` type
- Supports structured data (strings, numbers, lists, nested dicts)
- Has `.data` and `.metadata` properties

### Middleware System

**Two Types:**

1. **DownloaderMiddleware** - wraps HTTP download:
   - `process_request(request, spider)` - before download
   - `process_response(request, response, spider)` - after download
   - `process_exception(request, exception, spider)` - on error
   - All return `MiddlewareResult` (CONTINUE, KEEP, RETRY, DROP)

2. **SpiderMiddleware** - wraps spider processing:
   - `process_start_requests(start_requests, spider)` - filter initial requests
   - `process_spider_input(response, spider)` - before spider.parse()
   - `process_spider_output(response, result, spider)` - filter Items/Requests
   - `process_spider_exception(response, exception, spider)` - handle parse errors

**Middleware Resolution** (`_resolve_downloader_middleware`, `_resolve_spider_middleware`):
1. If class has `from_crawler(crawler)` classmethod → call it
2. If instance → use directly
3. If class → instantiate with `()`
4. If callable → try factory with `(settings)`, `(spider)`, or `()`

**Middleware Registration:**
- Defined in `Settings.DOWNLOADER_MIDDLEWARES` / `SPIDER_MIDDLEWARES` as `{"dotted.path": priority}`
- Lower priority number = executed first
- Middlewares are validated to have async hooks

### Type System Patterns

**Settings Typing:**
- `RuntimeSettings` is TYPE_CHECKING import of `Settings` class
- Use `Settings | dict[str, object] | None` for snapshot parameters
- `_build_final_settings()` always returns `RuntimeSettings` (Settings instance)

**Item Typing:**
- Items use `dict[str, object]` not `dict[str, str]`
- Allows scraped data to contain lists, numbers, nested structures
- Validation happens in pipelines, not at Item level

**Request Meta:**
- `request.meta: dict[str, object]`
- Common meta keys: `"proxy"` (str), `"retry_count"` (int), `"retry_delay"` (float)
- Always check types when accessing meta values

## Configuration Priority

Settings are merged with this precedence (lowest to highest):
1. **DEFAULT** - Library defaults from Settings dataclass
2. **CONFIG_FILE** - From TOML config file (.toml extension required)
3. **ENV** - Environment variables (QCRAWL_*)
4. **SPIDER** - Spider class/instance `custom_settings`
5. **CLI** - Command-line --setting arguments
6. **EXPLICIT** - Programmatic runtime overrides

Spider `custom_settings` can have mixed-case keys; they're normalized to UPPERCASE and merged using `Settings.with_overrides(filtered)`.

## Signals System

Uses a global signal dispatcher (`qcrawl.signals.signals_registry`):
- `spider_opened`, `spider_closed`
- `request_scheduled`, `request_reached_downloader`
- `response_received`, `bytes_received`
- `item_scraped`, `request_dropped`

Stats handlers connect to these for metrics collection.

## Important Implementation Details

**msgspec Usage:**
- Used for request serialization in scheduler queues (not for Items)
- Enables fast disk/Redis queue backends

**Queue System:**
- Priority queue with FIFO tiebreak
- Fingerprinting for deduplication using `RequestFingerprinter`
- Supports memory, disk, and Redis backends

**Concurrency Model:**
- Worker tasks spawn from `CrawlEngine.crawl()`
- Respects `CONCURRENCY` (global) and `CONCURRENCY_PER_DOMAIN` settings
- Managed by `ConcurrencyMiddleware` and `DownloadDelayMiddleware`

## Type Checking Notes

**Mypy Configuration:**
- Strict mode enabled with selective error code disabling
- `disable_error_code` includes: no-untyped-def, no-untyped-call, var-annotated, misc, attr-defined
- Always use TYPE_CHECKING imports for circular dependencies

**Common Patterns:**
- Use `# type: ignore[assignment]` for dynamic spider/engine wiring
- Assert non-None before accessing optional references (e.g., `assert self.engine is not None`)
- Settings always has `with_overrides()` method - no need for hasattr checks
