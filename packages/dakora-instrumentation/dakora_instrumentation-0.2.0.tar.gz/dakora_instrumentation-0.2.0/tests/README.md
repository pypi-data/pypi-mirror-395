# Tests for dakora-agents

This directory contains comprehensive tests for the `dakora-agents` package.

## Test Structure

- **`conftest.py`**: Pytest fixtures and test configuration
- **`test_middleware.py`**: Tests for `DakoraTraceMiddleware` class
- **`test_helpers.py`**: Tests for helper functions (`to_message`, etc.)
- **`test_integration.py`**: Integration tests simulating real-world usage

## Running Tests

### Run all tests

```bash
cd packages/agents
uv run pytest
```

### Run with coverage

```bash
uv run pytest --cov=dakora_agents --cov-report=html
```

### Run specific test file

```bash
uv run pytest tests/test_middleware.py
```

### Run specific test

```bash
uv run pytest tests/test_middleware.py::TestDakoraTraceMiddleware::test_middleware_initialization
```

### Run with verbose output

```bash
uv run pytest -v
```

## Test Coverage

The test suite covers:

### Middleware Tests (`test_middleware.py`)

- ✅ Initialization with required/optional parameters
- ✅ Trace metadata injection into context
- ✅ Trace creation with Dakora API
- ✅ Template metadata extraction and tracking
- ✅ Latency calculation
- ✅ Agent ID inclusion
- ✅ Error handling (graceful degradation)
- ✅ Conversation history preservation
- ✅ Helper function (`create_dakora_middleware`)

### Helper Tests (`test_helpers.py`)

- ✅ `to_message()` basic conversion
- ✅ Custom role assignment
- ✅ Metadata preservation
- ✅ Edge cases (empty metadata, different roles)

### Integration Tests (`test_integration.py`)

- ✅ Agent with middleware integration
- ✅ Complete template workflow (render → to_message → agent)
- ✅ Multi-turn conversations with session tracking
- ✅ Multi-agent workflows with shared sessions

## Adding New Tests

When adding new features to `dakora-agents`, please:

1. Add unit tests in the appropriate test file
2. Add integration tests if the feature involves multiple components
3. Update fixtures in `conftest.py` if needed
4. Run the full test suite before committing

## Mocking Strategy

Tests use `unittest.mock` to avoid requiring:

- Real Dakora server
- Real OpenAI API keys
- Real LLM calls

This makes tests:

- ✅ Fast (no network calls)
- ✅ Reliable (no external dependencies)
- ✅ Deterministic (consistent results)

## Known Test Coverage Gaps

While the current test suite provides solid coverage for core functionality, the following areas have limited or no test coverage:

### 1. Concurrent Requests

**Gap:** No tests for multiple simultaneous budget checks or agent executions.

**Why it matters:** Race conditions in the budget cache lock or concurrent OTEL span creation could cause issues in high-throughput applications.

**Mitigation:** The code uses `asyncio.Lock` with double-check locking pattern, which is well-tested in production environments. Manual testing with load tools (e.g., `locust`, `k6`) is recommended before deploying to high-concurrency environments.

**Future work:** Add tests using `asyncio.gather()` to simulate concurrent agent calls.

### 2. Network Timeout Scenarios

**Gap:** No tests for slow or hanging network requests to budget API or OTLP exporters.

**Why it matters:** Network timeouts could block agent execution or cause span export failures.

**Mitigation:** The code uses configurable timeouts (30s for OTLP exporter, exponential backoff with 10s max for budget checks). These defaults are conservative.

**Future work:** Add tests using `aioresponses` with delayed responses to verify timeout handling.

### 3. Edge Case Error Handling

**Gap:** Limited coverage for:

- Malformed JSON responses from Dakora API
- OTLP exporter failures during span export
- OpenTelemetry SDK version incompatibilities
- Corrupted or invalid budget cache data

**Why it matters:** These edge cases could cause silent failures or degraded observability.

**Mitigation:**

- Input validation on API responses (added in critical fixes)
- Exponential backoff retry logic (added in medium priority fixes)
- Version compatibility checks with warnings (added in medium priority fixes)
- Budget checks return safe defaults on errors (fail-open design)

**Future work:** Add parameterized tests for various API error responses and invalid data scenarios.

### 4. Integration with Real Services

**Gap:** All tests use mocks - no integration tests with actual Dakora API or OpenTelemetry backends.

**Why it matters:** Mock tests may not catch issues with real protocol implementations, authentication, or data serialization.

**Mitigation:** The package follows standard OpenTelemetry protocols (OTLP over HTTP) and uses well-tested libraries (`opentelemetry-sdk`, `opentelemetry-exporter-otlp-proto-http`).

**Recommended:** Before production deployment, run manual integration tests:

```bash
# Set up real Dakora API key
export DAKORA_API_KEY="dk_proj_..."

# Run example scripts with real services
python examples/01_quickstart/01_hello_world.py
python examples/03_maf_agents/01_simple_agent.py

# Verify traces appear in Dakora Studio
```

### 5. Performance and Memory Tests

**Gap:** No benchmarking or memory profiling tests.

**Why it matters:** Budget caching, span creation, and OTLP export could have performance implications at scale.

**Mitigation:** The middleware is designed to be lightweight with minimal overhead:

- Budget checks use aggressive caching (30s TTL)
- OTEL spans are batch-exported asynchronously
- No blocking operations in hot paths

**Recommended:** Profile your application with `py-spy` or `memray` before deploying to production.

## Test Quality Notes

Despite these gaps, the current test suite provides:

- ✅ **Strong unit test coverage** for core logic
- ✅ **Comprehensive input validation tests** for all public APIs
- ✅ **Error handling tests** for common failure modes
- ✅ **Integration tests** for typical usage patterns
- ✅ **Backwards compatibility tests** for API changes

The identified gaps are **edge cases and stress scenarios** that are difficult to test reliably in CI environments. For production deployments, supplement automated tests with:

1. Manual integration testing with real services
2. Load testing in staging environments
3. Canary deployments with monitoring
4. Gradual rollout with error rate tracking
