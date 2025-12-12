# Event-Driven Agent Triggering

Event-driven architecture allows Ceylon AI agents to respond dynamically to various events in your system, enabling reactive and scalable agent workflows.

## Overview

Event-driven agent triggering enables agents to:

- **React to external events** (webhooks, API calls, user actions)
- **Process asynchronous workloads** (message queues, database changes)
- **Schedule periodic tasks** (cron-like behavior)
- **Monitor system state** (logs, metrics, health checks)
- **Chain agent workflows** (agent-to-agent communication)

## Event Sources

Ceylon AI agents can be triggered from multiple event sources:

### 1. HTTP/Webhook Events

Expose agents via HTTP endpoints to handle external events:

```python
from ceylonai_next import LocalMesh, LlmAgent
import modal

app = modal.App("ceylon-webhook-agent")

@app.function()
@modal.web_endpoint(method="POST")
async def webhook_handler(request):
    """Handle incoming webhook events"""
    # Parse the event
    event_data = await request.json()

    # Spawn agent to process event
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name="webhook-processor",
        system_prompt="Process webhook events and extract insights",
        model_config={
            "provider": "openai",
            "model": "gpt-4"
        }
    )

    # Process the event
    result = await agent.run(
        f"Process this event: {event_data['type']}\nData: {event_data}"
    )

    return {"status": "processed", "result": result}
```

### 2. Scheduled Events

Trigger agents at specific intervals:

```python
from ceylonai_next import LocalMesh, LlmAgent
import modal

app = modal.App("ceylon-scheduled-agent")

@app.function()
@modal.period(hours=1)  # Run every hour
async def scheduled_task():
    """Periodic agent task"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name="monitor-agent",
        system_prompt="Monitor system health and report anomalies",
        model_config={
            "provider": "openai",
            "model": "gpt-4"
        }
    )

    result = await agent.run("Check system status and generate report")
    # Store or send the result
    return result

@app.function()
@modal.cron("0 9 * * *")  # Run daily at 9 AM
async def daily_summary():
    """Generate daily summary"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name="summary-agent",
        system_prompt="Generate comprehensive daily summaries",
        model_config={
            "provider": "openai",
            "model": "gpt-4"
        }
    )

    result = await agent.run("Generate daily summary report")
    return result
```

### 3. Message Queue Events

Process events from message queues:

```python
from ceylonai_next import LocalMesh, LlmAgent
import asyncio

async def process_queue_events(queue):
    """Process events from a message queue"""
    mesh = LocalMesh()

    while True:
        # Get event from queue
        event = await queue.get()

        # Spawn agent for this event
        agent = mesh.spawn_llm_agent(
            name=f"queue-processor-{event['id']}",
            system_prompt=f"Process {event['type']} events",
            model_config={
                "provider": "openai",
                "model": "gpt-4"
            }
        )

        # Process asynchronously
        result = await agent.run(f"Process: {event['data']}")

        # Mark as done
        queue.task_done()
```

### 4. Database Change Events

React to database changes:

```python
from ceylonai_next import LocalMesh, LlmAgent

class DatabaseEventHandler:
    def __init__(self):
        self.mesh = LocalMesh()

    async def on_insert(self, table: str, record: dict):
        """Trigger agent when new record is inserted"""
        agent = self.mesh.spawn_llm_agent(
            name=f"{table}-insert-handler",
            system_prompt=f"Process new {table} records and extract insights",
            model_config={
                "provider": "openai",
                "model": "gpt-4"
            }
        )

        result = await agent.run(
            f"New {table} record: {record}. Analyze and categorize."
        )
        return result

    async def on_update(self, table: str, old_record: dict, new_record: dict):
        """Trigger agent when record is updated"""
        agent = self.mesh.spawn_llm_agent(
            name=f"{table}-update-handler",
            system_prompt=f"Monitor {table} changes and detect anomalies",
            model_config={
                "provider": "openai",
                "model": "gpt-4"
            }
        )

        result = await agent.run(
            f"Record updated in {table}.\nOld: {old_record}\nNew: {new_record}\nAnalyze the change."
        )
        return result
```

### 5. Agent-to-Agent Events

Agents can trigger other agents through mesh networking:

```python
from ceylonai_next import LocalMesh, LlmAgent

# Create mesh
mesh = LocalMesh()

# Coordinator agent
coordinator = mesh.spawn_llm_agent(
    name="coordinator",
    system_prompt="Coordinate tasks and delegate to specialist agents",
    model_config={
        "provider": "openai",
        "model": "gpt-4"
    }
)

# Specialist agents
data_analyst = mesh.spawn_llm_agent(
    name="data-analyst",
    system_prompt="Analyze data and provide insights",
    model_config={
        "provider": "openai",
        "model": "gpt-4"
    }
)

report_writer = mesh.spawn_llm_agent(
    name="report-writer",
    system_prompt="Write comprehensive reports",
    model_config={
        "provider": "openai",
        "model": "gpt-4"
    }
)

# Coordinator delegates to specialists
async def process_request(user_request: str):
    # Coordinator decides what to do
    coordination_result = await coordinator.run(
        f"User request: {user_request}\nDetermine which specialist agents to involve."
    )

    # Trigger data analyst
    analysis = await data_analyst.run(f"Analyze: {user_request}")

    # Trigger report writer with analysis
    report = await report_writer.run(f"Write report based on: {analysis}")

    return report
```

## Event Patterns

### Fire-and-Forget

Trigger agents without waiting for results:

```python
import asyncio
from ceylonai_next import LocalMesh

async def fire_and_forget_agent(event_data):
    """Trigger agent without blocking"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name="background-processor",
        system_prompt="Process events in background",
        model_config={
            "provider": "openai",
            "model": "gpt-4"
        }
    )

    # Run in background task
    asyncio.create_task(agent.run(f"Process: {event_data}"))

    # Return immediately
    return {"status": "processing"}
```

### Request-Response

Wait for agent completion:

```python
async def request_response_agent(event_data):
    """Trigger agent and wait for result"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name="sync-processor",
        system_prompt="Process events and return results",
        model_config={
            "provider": "openai",
            "model": "gpt-4"
        }
    )

    # Wait for completion
    result = await agent.run(f"Process: {event_data}")

    return {"status": "completed", "result": result}
```

### Batch Processing

Process multiple events in batches:

```python
async def batch_process_events(events: list):
    """Process events in batches"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name="batch-processor",
        system_prompt="Process multiple events efficiently",
        model_config={
            "provider": "openai",
            "model": "gpt-4"
        }
    )

    # Process all events concurrently
    tasks = [
        agent.run(f"Process event: {event}")
        for event in events
    ]

    results = await asyncio.gather(*tasks)
    return results
```

### Event Filtering

Filter events before triggering agents:

```python
class EventFilter:
    def __init__(self, mesh: LocalMesh):
        self.mesh = mesh
        self.agent = None

    async def should_process(self, event: dict) -> bool:
        """Determine if event should trigger agent"""
        # Filter by type
        if event['type'] not in ['important', 'critical']:
            return False

        # Filter by priority
        if event.get('priority', 0) < 5:
            return False

        return True

    async def process_if_eligible(self, event: dict):
        """Process event if it passes filter"""
        if not await self.should_process(event):
            return {"status": "filtered"}

        if not self.agent:
            self.agent = self.mesh.spawn_llm_agent(
                name="filtered-processor",
                system_prompt="Process filtered high-priority events",
                model_config={
                    "provider": "openai",
                    "model": "gpt-4"
                }
            )

        result = await self.agent.run(f"Process: {event}")
        return {"status": "processed", "result": result}
```

## Best Practices

### 1. Error Handling

Always implement robust error handling for event-driven agents:

```python
async def resilient_event_handler(event):
    """Handle events with error recovery"""
    mesh = LocalMesh()
    max_retries = 3

    for attempt in range(max_retries):
        try:
            agent = mesh.spawn_llm_agent(
                name=f"resilient-agent-{attempt}",
                system_prompt="Process events reliably",
                model_config={
                    "provider": "openai",
                    "model": "gpt-4"
                }
            )

            result = await agent.run(f"Process: {event}")
            return {"status": "success", "result": result}

        except Exception as e:
            if attempt == max_retries - 1:
                return {"status": "failed", "error": str(e)}
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### 2. Resource Management

Manage agent lifecycle properly:

```python
class ManagedEventProcessor:
    def __init__(self):
        self.mesh = LocalMesh()
        self.active_agents = {}

    async def process_event(self, event_id: str, event_data: dict):
        """Process event with managed agent lifecycle"""
        try:
            # Create agent
            agent = self.mesh.spawn_llm_agent(
                name=f"processor-{event_id}",
                system_prompt="Process events efficiently",
                model_config={
                    "provider": "openai",
                    "model": "gpt-4"
                }
            )
            self.active_agents[event_id] = agent

            # Process
            result = await agent.run(f"Process: {event_data}")

            return result

        finally:
            # Cleanup
            if event_id in self.active_agents:
                del self.active_agents[event_id]
```

### 3. Monitoring and Logging

Track event processing with metrics:

```python
from ceylonai_next import LocalMesh, get_metrics

async def monitored_event_handler(event):
    """Process events with monitoring"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name="monitored-agent",
        system_prompt="Process events with tracking",
        model_config={
            "provider": "openai",
            "model": "gpt-4"
        }
    )

    # Process event
    result = await agent.run(f"Process: {event}")

    # Get metrics
    metrics = get_metrics()
    print(f"LLM Requests: {metrics['llm_requests']}")
    print(f"Total Tokens: {metrics['total_tokens']}")
    print(f"Estimated Cost: ${metrics['estimated_cost']:.4f}")

    return result
```

## Next Steps

- [Deployment Guide](../deployment/overview.md) - Deploy event-driven agents to production
- [Modal.com Integration](../deployment/modal.md) - Use Modal for serverless event processing
- [Async Best Practices](../async/best-practices.md) - Optimize async event handling
- [Metrics & Monitoring](../metrics/overview.md) - Monitor agent performance
