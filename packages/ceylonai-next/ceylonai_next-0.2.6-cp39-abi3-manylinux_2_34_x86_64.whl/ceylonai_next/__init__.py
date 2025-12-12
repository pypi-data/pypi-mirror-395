from .ceylonai_next import *
import inspect
import json
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


def _generate_schema_from_signature(func):
    """
    Generates a JSON schema from a function's type hints.
    """
    sig = inspect.signature(func)
    properties = {}
    required = []

    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        param_type = "string"  # Default to string
        if param.annotation != inspect.Parameter.empty:
            if param.annotation in type_map:
                param_type = type_map[param.annotation]
            # Handle Optional, List, etc. later if needed

        properties[name] = {"type": param_type}

        if param.default == inspect.Parameter.empty:
            required.append(name)

    schema = {
        "type": "object",
        "properties": properties,
    }
    if required:
        schema["required"] = required

    return json.dumps(schema)


class PyAction(_PyAction):
    def __new__(cls, name, description, input_schema=None, output_schema=None):
        if input_schema is None:
            input_schema = _generate_schema_from_signature(cls.execute)
        return super().__new__(cls, name, description, input_schema, output_schema)


class FunctionalAction(PyAction):
    def __new__(cls, func, name, description, input_schema=None, output_schema=None):
        # If input_schema is not provided, generate it from the function
        if input_schema is None:
            input_schema = _generate_schema_from_signature(func)
        # Create the instance using the parent's __new__
        instance = super().__new__(cls, name, description, input_schema, output_schema)
        # Store the function on the instance
        instance.func = func
        return instance

    def execute(self, context, inputs):
        # We need to map inputs to function arguments
        # For now, we assume inputs is a dict matching arguments
        # We also need to pass context if the function expects it

        sig = inspect.signature(self.func)
        kwargs = {}

        for name, param in sig.parameters.items():
            if name == "context":
                kwargs["context"] = context
            elif name in inputs:
                kwargs[name] = inputs[name]
            elif param.default != inspect.Parameter.empty:
                continue  # Use default
            else:
                # Missing argument
                pass

        return self.func(**kwargs)


class Agent(PyAgent):
    def __init__(self, name="agent"):
        super().__init__()
        self._agent_name = name
        self.tool_invoker = PyToolInvoker()
        self._last_response = None  # Store last response

    def name(self):
        return self._agent_name

    def action(self, name=None, description=""):
        def decorator(func):
            action_name = name or func.__name__
            action_desc = description or func.__doc__ or ""

            action = FunctionalAction(func, action_name, action_desc)
            self.tool_invoker.register(action)
            return func

        return decorator

    def on_message(self, message, context=None):
        """Handle incoming message. Override this method to process messages.

        Can be a synchronous method or an async method (async def).

        To return a response, return it from this method and it will be
        stored in _last_response.

        Args:
            message: The message content (bytes or string)
            context: Optional PyAgentContext

        Returns:
            Response string that will be stored
        """
        # Default implementation does nothing
        # Subclasses should override this
        return None

    def send_message(self, message):
        """Send a message to the agent and get the response.

        This wraps on_message and returns the response.

        Args:
            message: Message string to send

        Returns:
            Response from the agent's on_message handler
        """
        # Create a dummy context
        context = PyAgentContext("python")

        # Call on_message (which can be overridden by subclasses)
        response = self.on_message(message, context)

        # Store the response
        self._last_response = response

        return response if response is not None else "Message received"

    def last_response(self):
        """Get the last response from the agent.

        Returns:
            The last response string, or None if no messages sent yet
        """
        return self._last_response


class LocalMesh(PyLocalMesh):
    """Python wrapper for LocalMesh.

    Example:
        mesh = LocalMesh()
        agent = Agent("my_agent")
        mesh.register_agent(agent)
    """

    pass


class DistributedMesh(PyDistributedMesh):
    """Python wrapper for DistributedMesh.

    Example:
        # Server
        mesh = DistributedMesh("server_node", 50051)
        agent = Agent("my_agent")
        mesh.add_agent(agent)
        mesh.start()

        # Client
        client_mesh = DistributedMesh("client_node", 50052)
        client_mesh.start()
        client_mesh.send_to("my_agent", "Hello")
    """

    pass


class LlmConfig(PyLlmConfig):
    """Configuration for LLM Agent.
    
    Example:
        config = LlmConfig.builder() \\
            .provider("ollama") \\
            .model("llama3.2:latest") \\
            .temperature(0.7) \\
            .build()
    """

    pass


class LlmAgent(Agent):
    """Python wrapper for LlmAgent with fluent builder API.

    Example:
        # Builder style
        agent = LlmAgent("my_agent", "ollama::gemma3:latest")
        agent.with_system_prompt("You are a helpful assistant.")
        agent.build()

        # Config style
        config = LlmConfig.builder().provider("ollama").model("llama2").build()
        agent = LlmAgent(mesh, "my_agent", config)
    """

    def __new__(cls, *args, **kwargs):
        """Override __new__ to bypass PyAgent initialization.

        LlmAgent wraps PyLlmAgent internally, so it doesn't use Agent's initialization.
        We inherit from Agent only for type compatibility and interface consistency.
        """
        # Call parent __new__ without extra arguments to avoid PyAgent argument mismatch
        return Agent.__new__(cls)

    def __init__(self, name_or_mesh, model_or_name=None, config=None, memory=None):
        """Create a new LLM agent.

        Args:
            name_or_mesh: Agent name (str) OR Mesh instance
            model_or_name: Model string (str) OR Agent name (str) if first arg is mesh
            config: LlmConfig object (only if first arg is mesh)
            memory: InMemoryBackend object (optional)
        """
        if not isinstance(name_or_mesh, str):
            # Assumed to be a Mesh instance (duck typing)
            # Signature: (mesh, name, config, memory)
            self._mesh = name_or_mesh
            name = model_or_name
            self._config = config

            if not isinstance(name, str):
                raise ValueError("Agent name must be a string")

            if config is None:
                # Maybe model_or_name is actually the config and name is missing?
                # But let's stick to the example signature: (mesh, name, config)
                raise ValueError("Config is required when passing mesh")

            self._agent = PyLlmAgent.with_config(name, config)
            if memory:
                self._agent.with_memory(memory)
            # Auto-build since we have full config
            self._agent.build()
            self._built = True

            # Register with mesh if possible
            if hasattr(self._mesh, "register_agent"):
                self._mesh.register_agent(self._agent)

        else:
            # Signature: (name, model) or (name, config)
            name = name_or_mesh
            model_or_config = model_or_name

            # Check if the second argument is a Config object (duck typing or isinstance)
            # We check for 'inner' attribute which PyLlmConfig has, or if it's an instance of LlmConfig
            if isinstance(model_or_config, (LlmConfig, PyLlmConfig)):
                self._agent = PyLlmAgent.with_config(name, model_or_config)
            else:
                # Assume it's a model string
                self._agent = PyLlmAgent(name, model_or_config)

            if memory:
                self._agent.with_memory(memory)
            self._built = False

    def with_api_key(self, api_key):
        """Set the API key for the LLM provider."""
        self._agent.with_api_key(api_key)
        return self

    def with_system_prompt(self, prompt):
        """Set the system prompt for the agent."""
        self._agent.with_system_prompt(prompt)
        return self

    def with_temperature(self, temp):
        """Set the temperature for generation (0.0 - 2.0)."""
        self._agent.with_temperature(temp)
        return self

    def with_max_tokens(self, tokens):
        """Set the maximum number of tokens to generate."""
        self._agent.with_max_tokens(tokens)
        return self

    def with_memory(self, memory):
        """Set the memory backend for the agent."""
        self._agent.with_memory(memory)
        return self

    def build(self):
        """Build the agent. Must be called before sending messages."""
        self._agent.build()
        self._built = True
        return self

    def send_message(self, message):
        """Send a message to the agent."""
        if not self._built:
            raise RuntimeError("Agent not built. Call build() first.")
        return self._agent.send_message(message)

    async def send_message_async(self, message):
        """Send a message to the agent asynchronously."""
        if not self._built:
            raise RuntimeError("Agent not built. Call build() first.")
        return await self._agent.send_message_async(message)

    async def query_async(self, message):
        """Alias for send_message_async."""
        return await self.send_message_async(message)

    def register_action(self, action):
        """Register a Python action with the agent."""
        # We allow registering actions even if not built,
        # but the underlying agent needs to exist (which it does)
        # Fix: Use add_action instead of register_action to match Rust binding
        self._agent.add_action(action)
        return self

    def action(self, name=None, description=""):
        """Decorator to register a function as an action.

        Example:
            @agent.action(description="Get weather")
            def get_weather(location: str):
                return "Sunny"
        """

        def decorator(func):
            action_name = name or func.__name__
            action_desc = description or func.__doc__ or ""

            action = FunctionalAction(func, action_name, action_desc)
            self.register_action(action)
            return func

        return decorator

    def with_react(self, config=None):
        """Enable ReAct (Reason + Act) mode.

        Args:
            config: Optional ReActConfig. If None, uses default settings.

        Returns:
            Self for method chaining
        """
        if config is None:
            config = ReActConfig()
        self._agent.with_react(config._config)
        return self

    def send_message_react(self, message):
        """Send a message using ReAct reasoning mode.

        Returns:
            ReActResult with detailed reasoning trace
        """
        if not self._built:
            raise RuntimeError("Agent not built. Call build() first.")
        result = self._agent.send_message_react(message)
        return ReActResult(result)


class ReActConfig:
    """Configuration for ReAct (Reason + Act) mode."""

    def __init__(self):
        self._config = PyReActConfig()

    def with_max_iterations(self, max_iterations: int) -> "ReActConfig":
        """Set maximum reasoning iterations."""
        self._config.with_max_iterations(max_iterations)
        return self

    def with_thought_prefix(self, prefix: str) -> "ReActConfig":
        """Set the thought prefix (default: 'Thought:')."""
        self._config.with_thought_prefix(prefix)
        return self

    def with_action_prefix(self, prefix: str) -> "ReActConfig":
        """Set the action prefix (default: 'Action:')."""
        self._config.with_action_prefix(prefix)
        return self


class ReActStep:
    """A single step in the ReAct reasoning process."""

    def __init__(self, step):
        self._step = step

    @property
    def iteration(self) -> int:
        return self._step.iteration

    @property
    def thought(self) -> str:
        return self._step.thought

    @property
    def action(self) -> Optional[str]:
        return self._step.action

    @property
    def action_input(self) -> Optional[str]:
        return self._step.action_input

    @property
    def observation(self) -> Optional[str]:
        return self._step.observation

    def __repr__(self) -> str:
        return (
            f"ReActStep(iteration={self.iteration}, thought='{self.thought[:50]}...')"
        )


class ReActResult:
    """Result of a ReAct reasoning process."""

    def __init__(self, result):
        self._result = result

    @property
    def answer(self) -> str:
        """Final answer from reasoning process."""
        return self._result.answer

    @property
    def steps(self) -> List["ReActStep"]:
        """List of reasoning steps taken."""
        return [ReActStep(s) for s in self._result.get_steps()]

    @property
    def iterations(self) -> int:
        """Number of iterations performed."""
        return self._result.iterations

    @property
    def finish_reason(self) -> str:
        """Reason for finishing (Success/MaxIterations/Error)."""
        return self._result.finish_reason

    def print_trace(self) -> None:
        """Print the full reasoning trace."""
        print(f"ReAct Trace ({self.iterations} iterations)")
        print("=" * 60)
        for step in self.steps:
            print(f"\nIteration {step.iteration}:")
            print(f"Thought: {step.thought}")
            if step.action:
                print(f"Action: {step.action}[{step.action_input}]")
            if step.observation:
                print(f"Observation: {step.observation}")
        print("\n" + "=" * 60)
        print(f"Final Answer: {self.answer}")


class MemoryEntry(PyMemoryEntry):
    """Python wrapper for MemoryEntry with fluent API.

    Example:
        entry = MemoryEntry("Hello, world!")
        entry.with_metadata("type", "greeting")
        entry.with_metadata("user_id", "123")
        entry.with_ttl_seconds(3600)  # Expires in 1 hour
    """

    pass


class MemoryQuery(PyMemoryQuery):
    """Python wrapper for MemoryQuery with fluent API.

    Example:
        query = MemoryQuery()
        query.with_filter("type", "greeting")
        query.with_filter("user_id", "123")
        query.with_limit(10)
    """

    pass


class InMemoryBackend(PyInMemoryBackend):
    """Python wrapper for InMemoryBackend.

    Example:
        # Simple backend
        backend = InMemoryBackend()

        # With max entries limit (LRU eviction)
        backend = InMemoryBackend.with_max_entries(100)

        # With default TTL
        backend = InMemoryBackend.with_ttl_seconds(3600)

        # Store and retrieve
        entry = MemoryEntry("Hello, world!")
        entry_id = backend.store(entry)
        retrieved = backend.get(entry_id)
    """

    pass


class RedisBackend(PyRedisBackend):
    """Python wrapper for RedisBackend.

    Example:
        backend = RedisBackend("redis://localhost:6379")
        backend = backend.with_prefix("my_agent")
        backend = backend.with_ttl_seconds(3600)
    """

    pass


class Memory(ABC):
    """Abstract base class for custom memory backends.

    Extend this class to create custom memory implementations that can be used
    with LlmAgent. Useful for integrating vector databases, cloud storage, etc.

    Example:
        class VectorMemory(Memory):
            def __init__(self):
                self.vectors = {}

            def store(self, entry: MemoryEntry) -> str:
                # Store with vector embedding
                self.vectors[entry.id] = entry
                return entry.id

            def get(self, id: str) -> Optional[MemoryEntry]:
                return self.vectors.get(id)

            def search(self, query: MemoryQuery) -> List[MemoryEntry]:
                # Implement vector similarity search
                return list(self.vectors.values())

            def delete(self, id: str) -> bool:
                if id in self.vectors:
                    del self.vectors[id]
                    return True
                return False

            def clear(self):
                self.vectors.clear()

            def count(self) -> int:
                return len(self.vectors)

        # Use with agent
        agent = LlmAgent("agent", "model")
        agent.with_memory(VectorMemory())
    """

    @abstractmethod
    def store(self, entry: MemoryEntry) -> str:
        """Store a memory entry and return its ID."""
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[MemoryEntry]:
        """Retrieve a memory entry by ID."""
        pass

    @abstractmethod
    def search(self, query: MemoryQuery) -> List[MemoryEntry]:
        """Search for memory entries matching the query."""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete a memory entry. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def clear(self):
        """Clear all memory entries."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Return the number of entries in memory."""
        pass


class LoggingConfig(PyLoggingConfig):
    """Configuration for logging.

    Example:
        config = LoggingConfig("info", "ceylon.log", True)
    """

    pass


class LoggingHandle(PyLoggingHandle):
    """Handle to keep logging appenders alive."""

    pass


def init_logging(config: LoggingConfig) -> LoggingHandle:
    """Initialize logging with the given configuration.

    Args:
        config: LoggingConfig object

    Returns:
        LoggingHandle: Handle to keep logging active. Must be kept alive.
    """
    return init_logging_py(config)
