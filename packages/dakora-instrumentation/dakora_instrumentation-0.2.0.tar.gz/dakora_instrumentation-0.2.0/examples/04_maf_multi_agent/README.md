# Multi-Agent Examples

Examples showing multi-agent patterns with MAF and Dakora tracking.
All agents share the same middleware for unified observability.

## Examples

| File                      | Description                  | What You Learn                 |
| ------------------------- | ---------------------------- | ------------------------------ |
| `01_sequential_agents.py` | Research → Writer pipeline   | Sequential agent orchestration |
| `02_parallel_agents.py`   | Multiple agents in parallel  | Concurrent execution tracing   |
| `03_workflow_builder.py`  | WorkflowBuilder with routing | Conditional workflows          |

## Prerequisites

```bash
pip install 'dakora-instrumentation[maf]'
```

## Key Concepts

### Shared Middleware

All agents in a workflow share the same middleware instance:

```python
middleware = DakoraIntegration.setup(dakora)

researcher = ChatAgent(middleware=[middleware], ...)
writer = ChatAgent(middleware=[middleware], ...)
```

### Sequential Pipelines

Chain agents where one's output feeds the next:

```python
research = await researcher.run("Topic to research")
article = await writer.run(f"Write about: {research.text}")
```

### WorkflowBuilder

MAF's WorkflowBuilder enables conditional routing:

```python
workflow = (
    WorkflowBuilder()
    .set_start_executor(writer)
    .add_edge(writer, reviewer)
    .add_edge(reviewer, editor, condition=needs_editing)
    .add_edge(reviewer, publisher, condition=is_approved)
    .build()
)
```

### Trace Hierarchy

OTEL automatically creates parent-child relationships:

- Parent span: workflow execution
- Child spans: individual agent runs

View the complete flow in Dakora Studio's trace viewer.
