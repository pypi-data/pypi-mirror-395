# Advanced Examples

Production-ready patterns for advanced use cases.

## Examples

| File                      | Description                     | What You Learn           |
| ------------------------- | ------------------------------- | ------------------------ |
| `01_dual_export.py`       | Export to Dakora + Jaeger       | Multi-destination traces |
| `02_budget_checking.py`   | Pre-execution budget validation | Cost controls            |
| `03_custom_attributes.py` | Add custom span attributes      | Extended metadata        |

## Prerequisites

```bash
pip install 'dakora-instrumentation[maf]'

# For Jaeger example
docker run -d -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one
```

## Key Concepts

### Dual Export

Send traces to multiple backends simultaneously:

```python
middleware = DakoraIntegration.setup_with_jaeger(
    dakora,
    jaeger_endpoint="http://localhost:4317",
)
```

### Budget Checking

Validate budget before executing:

```python
middleware = DakoraIntegration.setup(
    dakora,
    budget_check_cache_ttl=30,  # Cache for 30s
)
# Budget is automatically checked before each execution
```

### Custom Attributes

Add business context to spans:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("customer.id", customer_id)
    span.set_attribute("workflow.type", "approval")
```
