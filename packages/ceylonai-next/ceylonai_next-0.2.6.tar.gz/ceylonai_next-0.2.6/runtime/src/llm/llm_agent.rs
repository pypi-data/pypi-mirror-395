use crate::core::action::{ActionInvoker, ActionMetadata, ToolInvoker};
use crate::core::agent::{Agent, AgentContext};
use crate::core::error::Result;
use crate::core::memory::{Memory, MemoryEntry, MemoryQuery};
use crate::core::message::Message as CeylonMessage;
use crate::llm::react::{ReActConfig, ReActEngine, ReActResult};
use crate::llm::types::{Message as LlmMessage, ToolSpec};
use crate::llm::{LLMClient, LLMConfig, LLMResponse, UniversalLLMClient};
use async_trait::async_trait;
use serde_json::{json, Value};
use std::sync::Arc;
use tokio::sync::Mutex;

/// An agent that uses an LLM (Large Language Model) to process messages.
///
/// The `LlmAgent` integrates with the Ceylon Mesh agent system and delegates
/// message processing to an LLM. It supports:
/// - Configurable system prompts
/// - Model parameters (temperature, max tokens, etc.)
/// - Tool calling integration with existing `ToolInvoker`
/// - Multiple LLM providers (OpenAI, Anthropic, Ollama, etc.)
/// - Optional memory module integration
///
/// # Examples
///
/// ```rust,no_run
/// use runtime::llm::{LlmAgent, LLMConfig};
///
/// // Create agent with Ollama (local, no API key needed)
/// let agent = LlmAgent::builder("my_agent", "ollama::llama2")
///     .with_system_prompt("You are a helpful assistant.")
///     .build()
///     .expect("Failed to create agent");
///
/// // Create agent with OpenAI
/// let agent = LlmAgent::builder("gpt_agent", "openai::gpt-4")
///     .with_api_key(std::env::var("OPENAI_API_KEY").unwrap())
///     .with_temperature(0.7)
///     .build()
///     .expect("Failed to create agent");
/// ```
pub struct LlmAgent {
    name: String,
    llm_client: UniversalLLMClient,
    llm_config: LLMConfig,
    system_prompt: String,
    conversation_history: Vec<LlmMessage>,
    tool_invoker: ToolInvoker,
    memory: Option<Arc<dyn Memory>>,
    react_config: Option<ReActConfig>,
}

impl LlmAgent {
    /// Create a builder for constructing an `LlmAgent`.
    ///
    /// # Arguments
    ///
    /// * `name` - The name of the agent
    /// * `model` - The model in "provider::model" format (e.g., "openai::gpt-4", "ollama::llama2")
    ///
    /// # Examples
    ///
    /// ```rust,no_run
    /// use runtime::llm::LlmAgent;
    ///
    /// let agent = LlmAgent::builder("my_agent", "ollama::llama2")
    ///     .build()
    ///     .expect("Failed to create agent");
    /// ```
    pub fn builder(name: impl Into<String>, model: impl Into<String>) -> LlmAgentBuilder {
        LlmAgentBuilder::new(name, model)
    }

    /// Create an LlmAgent with comprehensive LLMConfig
    pub fn new_with_config(
        name: impl Into<String>,
        config: LLMConfig,
        system_prompt: impl Into<String>,
        memory: Option<Arc<dyn Memory>>,
    ) -> Result<Self> {
        let client = UniversalLLMClient::new_with_config(config.clone())
            .map_err(|e| crate::core::error::Error::MeshError(e))?;

        let mut agent = Self {
            name: name.into(),
            llm_client: client,
            llm_config: config,
            system_prompt: system_prompt.into(),
            conversation_history: Vec::new(),
            tool_invoker: ToolInvoker::default(),
            memory,
            react_config: None,
        };

        // Register memory tools if memory is available
        if agent.memory.is_some() {
            agent.register_memory_tools();
        }

        Ok(agent)
    }

    /// Register memory-related tools
    fn register_memory_tools(&mut self) {
        if let Some(memory) = &self.memory {
            // Register save_memory tool
            self.tool_invoker
                .register(Box::new(SaveMemoryAction::new(memory.clone())));

            // Register search_memory tool
            self.tool_invoker
                .register(Box::new(SearchMemoryAction::new(memory.clone())));
        }
    }

    /// Convert Ceylon ActionMetadata to LLM ToolSpec
    fn action_to_tool_spec(action: &ActionMetadata) -> ToolSpec {
        ToolSpec {
            name: action.name.clone(),
            description: action.description.clone(),
            input_schema: action.input_schema.clone(),
        }
    }

    /// Enable ReAct (Reason + Act) mode
    pub fn with_react(&mut self, config: ReActConfig) {
        self.react_config = Some(config);
    }

    /// Send a message using ReAct reasoning mode
    pub async fn send_message_react(
        &mut self,
        message: impl Into<String>,
        ctx: &mut AgentContext,
    ) -> Result<ReActResult> {
        let content = message.into();

        // Check if ReAct is enabled
        let react_config = self.react_config.clone().ok_or_else(|| {
            crate::core::error::Error::MeshError(
                "ReAct mode not enabled. Call with_react() first".to_string(),
            )
        })?;

        // Create ReAct engine (without tool invoker for now)
        // TODO: Refactor to pass &mut ToolInvoker directly
        let engine = ReActEngine::new(react_config, None);

        // Execute ReAct loop
        let result = engine
            .execute(
                content,
                &self.llm_client,
                &self.llm_config,
                self.memory.as_ref(),
                ctx,
            )
            .await?;

        Ok(result)
    }

    /// Send a message and get the LLM's response
    /// This is a convenience method for Python bindings and direct usage.
    /// It processes the message with the LLM and returns the response text.
    pub async fn send_message_and_get_response(
        &mut self,
        message: impl Into<String>,
        ctx: &mut AgentContext,
    ) -> Result<String> {
        let content = message.into();

        // Add user message to conversation history
        self.conversation_history.push(LlmMessage {
            role: "user".to_string(),
            content,
        });

        // Process with LLM and return the response
        self.process_with_llm(ctx).await
    }

    /// Get the last assistant response from conversation history
    pub fn last_response(&self) -> Option<String> {
        self.conversation_history
            .iter()
            .rev()
            .find(|m| m.role == "assistant")
            .map(|m| m.content.clone())
    }

    /// Process incoming message with LLM and handle tool calls
    async fn process_with_llm(&mut self, ctx: &mut AgentContext) -> Result<String> {
        // Add system prompt to conversation if this is the first message
        if self.conversation_history.len() == 1 {
            self.conversation_history.insert(
                0,
                LlmMessage {
                    role: "system".to_string(),
                    content: self.system_prompt.clone(),
                },
            );
        }

        // Get available tools
        let actions = self.tool_invoker.list_actions();
        let tools: Vec<ToolSpec> = actions.iter().map(Self::action_to_tool_spec).collect();

        // Call LLM with conversation history and tools
        let response: LLMResponse<String> = self
            .llm_client
            .complete::<LLMResponse<String>, String>(&self.conversation_history, &tools)
            .await
            .map_err(|e| crate::core::error::Error::MeshError(e))?;

        // If LLM wants to use tools, execute them
        if !response.is_complete && !response.tool_calls.is_empty() {
            let mut tool_results = Vec::new();

            for tool_call in response.tool_calls {
                let result = self
                    .tool_invoker
                    .invoke(&tool_call.name, ctx, tool_call.input)
                    .await?;

                tool_results.push(format!("Tool {}: {}", tool_call.name, result));
            }

            // Add tool results to conversation
            let tool_result_message = LlmMessage {
                role: "tool".to_string(),
                content: tool_results.join("\n"),
            };
            self.conversation_history.push(tool_result_message);

            // Recursively call LLM again with tool results
            return Box::pin(self.process_with_llm(ctx)).await;
        }

        // Add assistant response to history
        self.conversation_history.push(LlmMessage {
            role: "assistant".to_string(),
            content: response.content.clone(),
        });

        Ok(response.content)
    }
}

#[async_trait]
impl Agent for LlmAgent {
    fn name(&self) -> String {
        self.name.clone()
    }

    async fn on_message(&mut self, msg: CeylonMessage, ctx: &mut AgentContext) -> Result<()> {
        // Convert payload bytes to string
        let content = String::from_utf8(msg.payload.clone()).map_err(|e| {
            crate::core::error::Error::MeshError(format!("Invalid UTF-8 in message payload: {}", e))
        })?;

        // Add user message to conversation history
        self.conversation_history.push(LlmMessage {
            role: "user".to_string(),
            content,
        });

        // Process with LLM
        let _response = self.process_with_llm(ctx).await?;
        Ok(())
    }

    async fn on_generic_message(
        &mut self,
        msg: crate::core::message::GenericMessage,
        ctx: &mut AgentContext,
    ) -> Result<crate::core::message::GenericResponse> {
        // Reuse existing send_message_and_get_response
        let response_text = self.send_message_and_get_response(msg.content, ctx).await?;
        Ok(crate::core::message::GenericResponse::new(response_text))
    }

    fn tool_invoker(&self) -> Option<&ToolInvoker> {
        Some(&self.tool_invoker)
    }

    fn tool_invoker_mut(&mut self) -> Option<&mut ToolInvoker> {
        Some(&mut self.tool_invoker)
    }
}

/// Builder for constructing an `LlmAgent` with fluent API.
pub struct LlmAgentBuilder {
    name: String,
    model: String,
    api_key: Option<String>,
    system_prompt: String,
    temperature: Option<f32>,
    max_tokens: Option<u32>,
    memory: Option<Arc<dyn Memory>>,
}

impl LlmAgentBuilder {
    fn new(name: impl Into<String>, model: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            model: model.into(),
            api_key: None,
            system_prompt: "You are a helpful AI assistant.".to_string(),
            temperature: None,
            max_tokens: None,
            memory: None,
        }
    }

    /// Set the API key for the LLM provider
    pub fn with_api_key(mut self, api_key: impl Into<String>) -> Self {
        self.api_key = Some(api_key.into());
        self
    }

    /// Set the system prompt for the agent
    pub fn with_system_prompt(mut self, prompt: impl Into<String>) -> Self {
        self.system_prompt = prompt.into();
        self
    }

    /// Set the temperature for generation (0.0 - 2.0)
    pub fn with_temperature(mut self, temperature: f32) -> Self {
        self.temperature = Some(temperature);
        self
    }

    /// Set the maximum number of tokens to generate
    pub fn with_max_tokens(mut self, max_tokens: u32) -> Self {
        self.max_tokens = Some(max_tokens);
        self
    }

    /// Set the memory backend
    pub fn with_memory(mut self, memory: Arc<dyn Memory>) -> Self {
        self.memory = Some(memory);
        self
    }

    /// Build the `LlmAgent`
    pub fn build(self) -> Result<LlmAgent> {
        // Create LLM config
        let mut config = LLMConfig::new(self.model);

        if let Some(api_key) = self.api_key {
            config = config.with_api_key(api_key);
        }

        if let Some(temperature) = self.temperature {
            config = config.with_temperature(temperature);
        }

        if let Some(max_tokens) = self.max_tokens {
            config = config.with_max_tokens(max_tokens);
        }

        LlmAgent::new_with_config(self.name, config, self.system_prompt, self.memory)
    }
}

// --- Built-in Memory Actions ---

struct SaveMemoryAction {
    memory: Arc<dyn Memory>,
    metadata: ActionMetadata,
}

impl SaveMemoryAction {
    fn new(memory: Arc<dyn Memory>) -> Self {
        Self {
            memory,
            metadata: ActionMetadata {
                name: "save_memory".to_string(),
                description: "Save information to memory for later retrieval.".to_string(),
                input_schema: json!({
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The information to save."
                        }
                    },
                    "required": ["content"]
                }),
                output_schema: Some(json!({
                    "type": "object",
                    "properties": {
                        "status": { "type": "string" },
                        "id": { "type": "string" }
                    }
                })),
            },
        }
    }
}

#[async_trait]
impl ActionInvoker for SaveMemoryAction {
    async fn execute(&self, _ctx: &mut AgentContext, inputs: Value) -> Result<Value> {
        let content = inputs
            .get("content")
            .and_then(|v| v.as_str())
            .ok_or_else(|| {
                crate::core::error::Error::ActionExecutionError(
                    "Missing 'content' in inputs".to_string(),
                )
            })?;

        let entry = MemoryEntry::new(content);
        let id = self.memory.store(entry).await?;

        Ok(json!({ "status": "success", "id": id }))
    }

    fn metadata(&self) -> &ActionMetadata {
        &self.metadata
    }
}

struct SearchMemoryAction {
    memory: Arc<dyn Memory>,
    metadata: ActionMetadata,
}

impl SearchMemoryAction {
    fn new(memory: Arc<dyn Memory>) -> Self {
        Self {
            memory,
            metadata: ActionMetadata {
                name: "search_memory".to_string(),
                description: "Search memory for relevant information.".to_string(),
                input_schema: json!({
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to search for."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Max number of results (default 5)."
                        }
                    },
                    "required": ["query"]
                }),
                output_schema: Some(json!({
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "array",
                            "items": { "type": "string" }
                        }
                    }
                })),
            },
        }
    }
}

#[async_trait]
impl ActionInvoker for SearchMemoryAction {
    async fn execute(&self, _ctx: &mut AgentContext, inputs: Value) -> Result<Value> {
        let query_str = inputs
            .get("query")
            .and_then(|v| v.as_str())
            .ok_or_else(|| {
                crate::core::error::Error::ActionExecutionError(
                    "Missing 'query' in inputs".to_string(),
                )
            })?;

        let limit = inputs
            .get("limit")
            .and_then(|v| v.as_u64())
            .map(|v| v as usize)
            .unwrap_or(5);

        let mut query = MemoryQuery::new().with_limit(limit);
        query.semantic_query = Some(query_str.to_string());

        let results = self.memory.search(query).await?;

        let result_strings: Vec<String> = results.into_iter().map(|e| e.content).collect();

        Ok(json!({ "results": result_strings }))
    }

    fn metadata(&self) -> &ActionMetadata {
        &self.metadata
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Note: Test removed because LlmAgent now directly uses UniversalLLMClient
    // instead of a trait object. For testing, you would need to startOllama or
    // mock at a different level.

    #[tokio::test]
    async fn test_llm_agent_builder() {
        // Test builder pattern with mock (this will use actual client)
        // We skip building the real client in test, just verify builder works
        let builder = LlmAgent::builder("test", "ollama::llama2")
            .with_system_prompt("Custom prompt")
            .with_temperature(0.7)
            .with_max_tokens(1000);

        // Just verify builder fields are set correctly
        assert_eq!(builder.name, "test");
        assert_eq!(builder.model, "ollama::llama2");
        assert_eq!(builder.system_prompt, "Custom prompt");
        assert_eq!(builder.temperature, Some(0.7));
        assert_eq!(builder.max_tokens, Some(1000));
    }
}
