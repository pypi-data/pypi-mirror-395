# Event-Driven Agent Examples

Practical examples demonstrating event-driven agent triggering patterns.

## Example 1: Webhook Event Handler

Complete implementation of a webhook-triggered agent system:

```python
from ceylonai_next import LocalMesh, LlmAgent
import modal
import os

app = modal.App("ceylon-webhook-demo")

# Create a persistent mesh for the app
mesh_instance = None

def get_mesh():
    """Get or create mesh instance"""
    global mesh_instance
    if mesh_instance is None:
        mesh_instance = LocalMesh()
    return mesh_instance

@app.function(
    secrets=[modal.Secret.from_name("openai-secret")]
)
@modal.web_endpoint(method="POST", label="webhook")
async def process_webhook(event_data: dict):
    """
    Process incoming webhook events with Ceylon AI agent

    Example webhook payload:
    {
        "type": "user_signup",
        "data": {
            "email": "user@example.com",
            "name": "John Doe"
        }
    }
    """
    mesh = get_mesh()

    # Spawn agent based on event type
    agent = mesh.spawn_llm_agent(
        name=f"webhook-{event_data['type']}-processor",
        system_prompt=f"""You are a webhook event processor for {event_data['type']} events.
        Analyze the event and determine appropriate actions.""",
        model_config={
            "provider": "openai",
            "model": "gpt-4",
            "api_key": os.environ["OPENAI_API_KEY"]
        }
    )

    # Process the event
    prompt = f"""
    Event Type: {event_data['type']}
    Event Data: {event_data.get('data', {})}

    Please:
    1. Validate the event data
    2. Determine required actions
    3. Provide a structured response
    """

    result = await agent.run(prompt)

    return {
        "status": "processed",
        "event_type": event_data['type'],
        "result": result
    }

@app.function(
    secrets=[modal.Secret.from_name("openai-secret")]
)
@modal.web_endpoint(method="GET", label="health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ceylon-webhook-agent"}
```

## Example 2: Scheduled Data Analysis

Periodic agent for data analysis and reporting:

```python
from ceylonai_next import LocalMesh, LlmAgent, get_metrics
import modal
import os
from datetime import datetime

app = modal.App("ceylon-scheduled-analyzer")

@app.function(
    secrets=[modal.Secret.from_name("openai-secret")],
    schedule=modal.Period(hours=1)  # Run every hour
)
async def hourly_analysis():
    """Analyze system metrics every hour"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name=f"analyzer-{datetime.now().isoformat()}",
        system_prompt="""You are a data analyst agent.
        Analyze system metrics and identify trends, anomalies, and insights.""",
        model_config={
            "provider": "openai",
            "model": "gpt-4",
            "api_key": os.environ["OPENAI_API_KEY"]
        }
    )

    # Simulate fetching metrics
    system_metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": 45.2,
        "memory_usage": 62.8,
        "active_users": 127,
        "requests_per_minute": 450
    }

    result = await agent.run(f"""
    Analyze these system metrics:
    {system_metrics}

    Provide:
    1. Overall health assessment
    2. Trend analysis
    3. Anomaly detection
    4. Recommendations
    """)

    # Get agent metrics
    agent_metrics = get_metrics()

    print(f"Analysis complete at {datetime.now()}")
    print(f"LLM Cost: ${agent_metrics['estimated_cost']:.4f}")

    return {
        "timestamp": datetime.now().isoformat(),
        "analysis": result,
        "agent_cost": agent_metrics['estimated_cost']
    }

@app.function(
    secrets=[modal.Secret.from_name("openai-secret")],
    schedule=modal.Cron("0 9 * * *")  # 9 AM daily
)
async def daily_report():
    """Generate daily summary report"""
    mesh = LocalMesh()
    agent = mesh.spawn_llm_agent(
        name=f"daily-reporter-{datetime.now().date()}",
        system_prompt="""You are a report generation agent.
        Create comprehensive daily summaries with insights and recommendations.""",
        model_config={
            "provider": "openai",
            "model": "gpt-4",
            "api_key": os.environ["OPENAI_API_KEY"]
        }
    )

    result = await agent.run("""
    Generate a daily summary report including:
    1. Key metrics from the past 24 hours
    2. Notable events or anomalies
    3. Performance trends
    4. Action items for today
    """)

    return {
        "date": datetime.now().date().isoformat(),
        "report": result
    }
```

## Example 3: Multi-Agent Event Pipeline

Chain multiple agents for complex event processing:

```python
from ceylonai_next import LocalMesh, LlmAgent
import asyncio

class EventPipeline:
    """Multi-stage event processing pipeline"""

    def __init__(self):
        self.mesh = LocalMesh()
        self.agents = {}

    def create_agent(self, role: str, system_prompt: str) -> LlmAgent:
        """Create specialized agent for pipeline stage"""
        if role not in self.agents:
            self.agents[role] = self.mesh.spawn_llm_agent(
                name=f"pipeline-{role}",
                system_prompt=system_prompt,
                model_config={
                    "provider": "openai",
                    "model": "gpt-4"
                }
            )
        return self.agents[role]

    async def validate(self, event: dict) -> dict:
        """Stage 1: Validate event"""
        validator = self.create_agent(
            "validator",
            "Validate event data and ensure it meets requirements."
        )

        result = await validator.run(f"""
        Validate this event:
        {event}

        Check for:
        - Required fields
        - Data types
        - Valid ranges

        Return: {{valid: bool, errors: list}}
        """)

        return {"stage": "validation", "result": result}

    async def enrich(self, event: dict) -> dict:
        """Stage 2: Enrich event with additional data"""
        enricher = self.create_agent(
            "enricher",
            "Enrich events with contextual information and metadata."
        )

        result = await enricher.run(f"""
        Enrich this event with additional context:
        {event}

        Add:
        - Timestamp
        - Category
        - Priority
        - Related entities
        """)

        return {"stage": "enrichment", "result": result}

    async def analyze(self, event: dict) -> dict:
        """Stage 3: Analyze event"""
        analyzer = self.create_agent(
            "analyzer",
            "Analyze events and extract insights."
        )

        result = await analyzer.run(f"""
        Analyze this event:
        {event}

        Provide:
        - Key insights
        - Patterns
        - Anomalies
        - Recommendations
        """)

        return {"stage": "analysis", "result": result}

    async def route(self, event: dict, analysis: dict) -> dict:
        """Stage 4: Route based on analysis"""
        router = self.create_agent(
            "router",
            "Route events to appropriate handlers based on analysis."
        )

        result = await router.run(f"""
        Event: {event}
        Analysis: {analysis}

        Determine:
        - Target handler
        - Priority
        - Actions required
        """)

        return {"stage": "routing", "result": result}

    async def process_event(self, event: dict) -> dict:
        """Process event through complete pipeline"""
        try:
            # Run stages sequentially
            validation = await self.validate(event)
            if "error" in validation:
                return validation

            enrichment = await self.enrich(event)
            analysis = await self.analyze(enrichment)
            routing = await self.route(event, analysis)

            return {
                "status": "success",
                "pipeline_results": {
                    "validation": validation,
                    "enrichment": enrichment,
                    "analysis": analysis,
                    "routing": routing
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

# Usage
async def main():
    pipeline = EventPipeline()

    event = {
        "type": "user_action",
        "action": "login",
        "user_id": "12345",
        "timestamp": "2024-12-04T10:00:00Z"
    }

    result = await pipeline.process_event(event)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 4: Event Queue Consumer

Process events from a queue with concurrency control:

```python
from ceylonai_next import LocalMesh, LlmAgent
import asyncio
from asyncio import Queue
from typing import List

class QueueEventProcessor:
    """Process events from queue with controlled concurrency"""

    def __init__(self, max_concurrent: int = 5):
        self.mesh = LocalMesh()
        self.max_concurrent = max_concurrent
        self.queue = Queue()
        self.results = []

    async def worker(self, worker_id: int):
        """Worker that processes events from queue"""
        while True:
            # Get event from queue
            event = await self.queue.get()

            if event is None:  # Sentinel for shutdown
                self.queue.task_done()
                break

            try:
                # Create agent for this event
                agent = self.mesh.spawn_llm_agent(
                    name=f"worker-{worker_id}-event-{event['id']}",
                    system_prompt="Process queued events efficiently",
                    model_config={
                        "provider": "openai",
                        "model": "gpt-4"
                    }
                )

                # Process event
                result = await agent.run(f"Process event: {event}")

                self.results.append({
                    "event_id": event['id'],
                    "worker_id": worker_id,
                    "status": "success",
                    "result": result
                })

            except Exception as e:
                self.results.append({
                    "event_id": event.get('id', 'unknown'),
                    "worker_id": worker_id,
                    "status": "error",
                    "error": str(e)
                })

            finally:
                self.queue.task_done()

    async def process_events(self, events: List[dict]):
        """Process list of events with workers"""
        # Add events to queue
        for event in events:
            await self.queue.put(event)

        # Create workers
        workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.max_concurrent)
        ]

        # Wait for all events to be processed
        await self.queue.join()

        # Shutdown workers
        for _ in range(self.max_concurrent):
            await self.queue.put(None)

        # Wait for workers to finish
        await asyncio.gather(*workers)

        return self.results

# Usage
async def main():
    processor = QueueEventProcessor(max_concurrent=3)

    events = [
        {"id": i, "type": "data_update", "data": f"event_{i}"}
        for i in range(10)
    ]

    results = await processor.process_events(events)

    print(f"Processed {len(results)} events")
    successful = sum(1 for r in results if r['status'] == 'success')
    print(f"Successful: {successful}/{len(results)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 5: Real-time Event Monitoring

Monitor events and trigger agents based on patterns:

```python
from ceylonai_next import LocalMesh, LlmAgent
import asyncio
from collections import deque
from datetime import datetime, timedelta

class EventMonitor:
    """Monitor event stream and trigger agents for patterns"""

    def __init__(self, window_size: int = 100):
        self.mesh = LocalMesh()
        self.event_window = deque(maxlen=window_size)
        self.alert_agent = None

    def add_event(self, event: dict):
        """Add event to monitoring window"""
        event['received_at'] = datetime.now()
        self.event_window.append(event)

    def detect_anomaly(self) -> bool:
        """Simple anomaly detection"""
        if len(self.event_window) < 10:
            return False

        # Check for error spike
        recent_errors = sum(
            1 for e in list(self.event_window)[-10:]
            if e.get('level') == 'error'
        )

        return recent_errors >= 5

    def detect_pattern(self, pattern_type: str) -> bool:
        """Detect specific patterns in event window"""
        recent = list(self.event_window)[-20:]

        if pattern_type == "high_frequency":
            # Check if events are too frequent
            if len(recent) >= 20:
                time_span = (recent[-1]['received_at'] -
                           recent[0]['received_at']).total_seconds()
                return time_span < 10  # 20 events in 10 seconds

        return False

    async def handle_anomaly(self, anomaly_type: str):
        """Trigger agent to handle detected anomaly"""
        if not self.alert_agent:
            self.alert_agent = self.mesh.spawn_llm_agent(
                name="alert-handler",
                system_prompt="""You are an alert handler agent.
                Analyze anomalies and recommend actions.""",
                model_config={
                    "provider": "openai",
                    "model": "gpt-4"
                }
            )

        recent_events = list(self.event_window)[-20:]

        result = await self.alert_agent.run(f"""
        ANOMALY DETECTED: {anomaly_type}

        Recent events:
        {recent_events}

        Please:
        1. Analyze the situation
        2. Determine severity
        3. Recommend immediate actions
        4. Suggest preventive measures
        """)

        return {
            "anomaly_type": anomaly_type,
            "timestamp": datetime.now().isoformat(),
            "analysis": result,
            "event_count": len(recent_events)
        }

    async def monitor(self):
        """Continuous monitoring loop"""
        while True:
            # Check for anomalies
            if self.detect_anomaly():
                alert = await self.handle_anomaly("error_spike")
                print(f"ALERT: {alert}")

            # Check for patterns
            if self.detect_pattern("high_frequency"):
                alert = await self.handle_anomaly("high_frequency")
                print(f"ALERT: {alert}")

            await asyncio.sleep(5)  # Check every 5 seconds

# Usage
async def main():
    monitor = EventMonitor()

    # Start monitoring in background
    monitor_task = asyncio.create_task(monitor.monitor())

    # Simulate events
    for i in range(100):
        event = {
            "id": i,
            "level": "error" if i % 10 == 0 else "info",
            "message": f"Event {i}"
        }
        monitor.add_event(event)
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())
```

## Next Steps

- [Event Overview](overview.md) - Learn about event-driven patterns
- [Deployment Guide](../deployment/modal.md) - Deploy to Modal.com
- [Async Best Practices](../async/best-practices.md) - Optimize performance
