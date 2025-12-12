//! LLM (Large Language Model) integration layer.
//!
//! This module provides a unified interface for interacting with various LLM providers
//! including OpenAI, Anthropic, Ollama, Google, and many others.
//!
//! # Supported Providers
//!
//! Ceylon supports 13+ LLM providers through the [`UniversalLLMClient`]:
//!
//! - **OpenAI** - GPT-4, GPT-3.5-turbo, etc.
//! - **Anthropic** - Claude 3 Opus, Sonnet, Haiku
//! - **Ollama** - Local models (Llama, Mistral, Gemma, etc.)
//! - **Google** - Gemini Pro
//! - **DeepSeek** - DeepSeek Chat, DeepSeek Coder
//! - **X.AI** - Grok
//! - **Groq** - High-speed inference
//! - **Azure OpenAI** - Enterprise OpenAI deployment
//! - **Cohere** - Command models
//! - **Mistral** - Mistral AI models
//! - **Phind** - CodeLlama variants
//! - **OpenRouter** - Multi-provider routing
//! - **ElevenLabs** - Voice/audio generation
//!
//! # Configuration
//!
//! Use [`LLMConfig`] for comprehensive configuration:
//!
//! ```rust,no_run
//! use runtime::llm::LLMConfig;
//!
//! let config = LLMConfig::new("openai::gpt-4")
//!     .with_api_key("sk-...")
//!     .with_temperature(0.7)
//!     .with_max_tokens(2048)
//!     .with_resilience(true, 3);
//! ```
//!
//! # API Key Detection
//!
//! Ceylon automatically detects API keys from environment variables:
//! - `OPENAI_API_KEY`
//! - `ANTHROPIC_API_KEY`
//! - `GOOGLE_API_KEY`
//! - `DEEPSEEK_API_KEY`
//! - `XAI_API_KEY`
//! - `GROQ_API_KEY`
//! - `MISTRAL_API_KEY`
//! - `COHERE_API_KEY`
//! - `PHIND_API_KEY`
//! - `OPENROUTER_API_KEY`
//! - And more...
//!
//! # Tool Calling
//!
//! Ceylon supports native tool calling for compatible models and falls back to
//! text-based tool invocation for others.
//!
//! # Examples
//!
//! ## Basic Usage
//!
//! ```rust,no_run
//! use runtime::llm::{UniversalLLMClient, LLMClient, LLMResponse};
//! use runtime::llm::types::Message;
//!
//! # async fn example() -> Result<(), String> {
//! let client = UniversalLLMClient::new("openai::gpt-4", None)?;
//! let messages = vec![Message {
//!     role: "user".to_string(),
//!     content: "Hello!".to_string(),
//! }];
//!
//! let response: LLMResponse<String> = client
//!     .complete::<LLMResponse<String>, String>(&messages, &[])
//!     .await?;
//! # Ok(())
//! # }
//! ```
//!
//! ## Advanced Configuration
//!
//! ```rust,no_run
//! use runtime::llm::{LLMConfig, UniversalLLMClient};
//!
//! # fn example() -> Result<(), String> {
//! let llm_config = LLMConfig::new("anthropic::claude-3-opus-20240229")
//!     .with_api_key(std::env::var("ANTHROPIC_API_KEY").unwrap())
//!     .with_temperature(0.8)
//!     .with_max_tokens(4096)
//!     .with_reasoning(true);
//!
//! let client = UniversalLLMClient::new_with_config(llm_config)?;
//! # Ok(())
//! # }
//! ```
//!
//! ## Local Models with Ollama
//!
//! ```rust,no_run
//! use runtime::llm::UniversalLLMClient;
//!
//! # fn example() -> Result<(), String> {
//! // No API key needed for local models
//! let client = UniversalLLMClient::new("ollama::llama2", None)?;
//! # Ok(())
//! # }
//! ```

pub mod llm_agent;
pub mod react;
pub mod types;

pub use llm_agent::{LlmAgent, LlmAgentBuilder};
pub use react::{FinishReason, ReActConfig, ReActEngine, ReActResult, ReActStep};

use async_trait::async_trait;
use llm::builder::{LLMBackend, LLMBuilder};
use llm::chat::ChatMessage;
use llm::LLMProvider;
use serde::{Deserialize, Serialize};
use types::{Message, ToolSpec};

// ============================================================================
// LLM CLIENT - Talks to actual LLM API
// ============================================================================

/// Trait for LLM response types with tool calling support.
///
/// This trait defines the interface for LLM responses, supporting both
/// content generation and tool calling capabilities.
pub trait LLMResponseTrait<C: for<'de> Deserialize<'de> + Default + Send> {
    /// Creates a new LLM response.
    fn new(content: C, tool_calls: Vec<ToolCall>, is_complete: bool) -> Self;

    /// Returns whether the response is complete.
    fn is_complete(&self) -> bool;

    /// Returns the tool calls requested by the LLM.
    fn tool_calls(&self) -> Vec<ToolCall>;

    /// Returns the content of the response.
    fn content(&self) -> C;
}

/// Response from an LLM including generated content and tool calls.
///
/// This struct represents a complete response from an LLM, which may include
/// generated text content and/or requests to call tools.
///
/// # Examples
///
/// ```rust,no_run
/// use runtime::llm::{LLMResponse, ToolCall};
///
/// let response = LLMResponse {
///     content: "Let me calculate that for you".to_string(),
///     tool_calls: vec![
///         ToolCall {
///             name: "calculator".to_string(),
///             input: serde_json::json!({"operation": "add", "a": 2, "b": 2}),
///         }
///     ],
///     is_complete: false,
/// };
/// ```
#[derive(Debug, Clone, Serialize, Default)]
pub struct LLMResponse<C>
where
    C: for<'de> Deserialize<'de> + Default + Clone + Send,
{
    /// The generated content from the LLM
    pub content: C,

    /// Tool calls requested by the LLM (supports multiple calls)
    pub tool_calls: Vec<ToolCall>,

    /// Whether the response is complete (false if tool calls need to be executed)
    pub is_complete: bool,
}

impl<C> LLMResponseTrait<C> for LLMResponse<C>
where
    C: for<'de> Deserialize<'de> + Default + Clone + Send,
{
    fn new(content: C, tool_calls: Vec<ToolCall>, is_complete: bool) -> Self {
        Self {
            content,
            tool_calls,
            is_complete,
        }
    }

    fn is_complete(&self) -> bool {
        self.is_complete
    }

    fn tool_calls(&self) -> Vec<ToolCall> {
        self.tool_calls.clone()
    }

    fn content(&self) -> C {
        self.content.clone()
    }
}

/// A request from the LLM to call a tool.
///
/// When an LLM wants to use a tool to perform an action, it returns a `ToolCall`
/// specifying which tool to invoke and with what parameters.
///
/// # Examples
///
/// ```rust
/// use runtime::llm::ToolCall;
/// use serde_json::json;
///
/// let tool_call = ToolCall {
///     name: "search_database".to_string(),
///     input: json!({
///         "query": "users with age > 30",
///         "limit": 10
///     }),
/// };
/// ```
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolCall {
    /// The name of the tool to call
    pub name: String,

    /// The input parameters for the tool as a JSON value
    pub input: serde_json::Value,
}

/// Configuration for LLM providers with all builder options.
///
/// This struct provides comprehensive configuration for any LLM provider,
/// matching all options available in the LLMBuilder.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LLMConfig {
    // Basic configuration
    pub model: String,
    pub api_key: Option<String>,
    pub base_url: Option<String>,

    // Generation parameters
    pub max_tokens: Option<u32>,
    pub temperature: Option<f32>,
    pub top_p: Option<f32>,
    pub top_k: Option<u32>,
    pub system: Option<String>,

    // Timeout and retry
    pub timeout_seconds: Option<u64>,

    // Embeddings
    pub embedding_encoding_format: Option<String>,
    pub embedding_dimensions: Option<u32>,

    // Tools and function calling
    pub enable_parallel_tool_use: Option<bool>,

    // Reasoning (for providers that support it)
    pub reasoning: Option<bool>,
    pub reasoning_effort: Option<String>,
    pub reasoning_budget_tokens: Option<u32>,

    // Provider-specific: Azure
    pub api_version: Option<String>,
    pub deployment_id: Option<String>,

    // Provider-specific: Voice/Audio
    pub voice: Option<String>,

    // Provider-specific: XAI search
    pub xai_search_mode: Option<String>,
    pub xai_search_source_type: Option<String>,
    pub xai_search_excluded_websites: Option<Vec<String>>,
    pub xai_search_max_results: Option<u32>,
    pub xai_search_from_date: Option<String>,
    pub xai_search_to_date: Option<String>,

    // Provider-specific: OpenAI web search
    pub openai_enable_web_search: Option<bool>,
    pub openai_web_search_context_size: Option<String>,
    pub openai_web_search_user_location_type: Option<String>,
    pub openai_web_search_user_location_approximate_country: Option<String>,
    pub openai_web_search_user_location_approximate_city: Option<String>,
    pub openai_web_search_user_location_approximate_region: Option<String>,

    // Resilience
    pub resilient_enable: Option<bool>,
    pub resilient_attempts: Option<usize>,
    pub resilient_base_delay_ms: Option<u64>,
    pub resilient_max_delay_ms: Option<u64>,
    pub resilient_jitter: Option<bool>,
}

impl Default for LLMConfig {
    fn default() -> Self {
        Self {
            model: String::new(),
            api_key: None,
            base_url: None,
            max_tokens: Some(4096),
            temperature: None,
            top_p: None,
            top_k: None,
            system: None,
            timeout_seconds: None,
            embedding_encoding_format: None,
            embedding_dimensions: None,
            enable_parallel_tool_use: None,
            reasoning: None,
            reasoning_effort: None,
            reasoning_budget_tokens: None,
            api_version: None,
            deployment_id: None,
            voice: None,
            xai_search_mode: None,
            xai_search_source_type: None,
            xai_search_excluded_websites: None,
            xai_search_max_results: None,
            xai_search_from_date: None,
            xai_search_to_date: None,
            openai_enable_web_search: None,
            openai_web_search_context_size: None,
            openai_web_search_user_location_type: None,
            openai_web_search_user_location_approximate_country: None,
            openai_web_search_user_location_approximate_city: None,
            openai_web_search_user_location_approximate_region: None,
            resilient_enable: None,
            resilient_attempts: None,
            resilient_base_delay_ms: None,
            resilient_max_delay_ms: None,
            resilient_jitter: None,
        }
    }
}

impl LLMConfig {
    /// Create a new LLMConfig with just the model name
    pub fn new(model: impl Into<String>) -> Self {
        Self {
            model: model.into(),
            ..Default::default()
        }
    }

    /// Set API key
    pub fn with_api_key(mut self, api_key: impl Into<String>) -> Self {
        self.api_key = Some(api_key.into());
        self
    }

    /// Set base URL
    pub fn with_base_url(mut self, base_url: impl Into<String>) -> Self {
        self.base_url = Some(base_url.into());
        self
    }

    /// Set max tokens
    pub fn with_max_tokens(mut self, max_tokens: u32) -> Self {
        self.max_tokens = Some(max_tokens);
        self
    }

    /// Set temperature
    pub fn with_temperature(mut self, temperature: f32) -> Self {
        self.temperature = Some(temperature);
        self
    }

    /// Set top_p
    pub fn with_top_p(mut self, top_p: f32) -> Self {
        self.top_p = Some(top_p);
        self
    }

    /// Set top_k
    pub fn with_top_k(mut self, top_k: u32) -> Self {
        self.top_k = Some(top_k);
        self
    }

    /// Set system prompt
    pub fn with_system(mut self, system: impl Into<String>) -> Self {
        self.system = Some(system.into());
        self
    }

    /// Set timeout in seconds
    pub fn with_timeout_seconds(mut self, timeout: u64) -> Self {
        self.timeout_seconds = Some(timeout);
        self
    }

    /// Enable reasoning (for supported providers)
    pub fn with_reasoning(mut self, enabled: bool) -> Self {
        self.reasoning = Some(enabled);
        self
    }

    /// Set reasoning effort
    pub fn with_reasoning_effort(mut self, effort: impl Into<String>) -> Self {
        self.reasoning_effort = Some(effort.into());
        self
    }

    /// Set Azure deployment ID
    pub fn with_deployment_id(mut self, deployment_id: impl Into<String>) -> Self {
        self.deployment_id = Some(deployment_id.into());
        self
    }

    /// Set Azure API version
    pub fn with_api_version(mut self, api_version: impl Into<String>) -> Self {
        self.api_version = Some(api_version.into());
        self
    }

    /// Enable OpenAI web search
    pub fn with_openai_web_search(mut self, enabled: bool) -> Self {
        self.openai_enable_web_search = Some(enabled);
        self
    }

    /// Enable resilience with retry/backoff
    pub fn with_resilience(mut self, enabled: bool, attempts: usize) -> Self {
        self.resilient_enable = Some(enabled);
        self.resilient_attempts = Some(attempts);
        self
    }
}

/// Legacy config for backward compatibility
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LLMProviderConfig {
    pub model: String,
    pub max_tokens: u64,
    pub api_key: Option<String>,
    pub base_url: String,
}

impl From<LLMConfig> for LLMProviderConfig {
    fn from(config: LLMConfig) -> Self {
        Self {
            model: config.model,
            max_tokens: config.max_tokens.unwrap_or(4096) as u64,
            api_key: config.api_key,
            base_url: config.base_url.unwrap_or_default(),
        }
    }
}

/// Get the environment variable name for a provider's API key
fn get_api_key_env_var(provider: &str) -> Option<&'static str> {
    match provider.to_lowercase().as_str() {
        "ollama" => None, // Ollama doesn't require API key
        "anthropic" | "claude" => Some("ANTHROPIC_API_KEY"),
        "openai" | "gpt" => Some("OPENAI_API_KEY"),
        "deepseek" => Some("DEEPSEEK_API_KEY"),
        "xai" | "x.ai" => Some("XAI_API_KEY"),
        "phind" => Some("PHIND_API_KEY"),
        "google" | "gemini" => Some("GOOGLE_API_KEY"),
        "groq" => Some("GROQ_API_KEY"),
        "azure" | "azureopenai" | "azure-openai" => Some("AZURE_OPENAI_API_KEY"),
        "elevenlabs" | "11labs" => Some("ELEVENLABS_API_KEY"),
        "cohere" => Some("COHERE_API_KEY"),
        "mistral" => Some("MISTRAL_API_KEY"),
        "openrouter" => Some("OPENROUTER_API_KEY"),
        _ => None,
    }
}

/// Attempt to get API key from environment variable for the provider
/// Returns Ok(Some(key)) if found, Ok(None) if provider doesn't need key, Err if required but not found
fn get_api_key_from_env(provider: &str) -> Result<Option<String>, String> {
    match get_api_key_env_var(provider) {
        None => Ok(None), // Provider doesn't need API key
        Some(env_var) => {
            match std::env::var(env_var) {
                Ok(key) => Ok(Some(key)),
                Err(_) => Err(format!(
                    "API key required for provider '{}'. Please set the {} environment variable or pass the API key explicitly.",
                    provider, env_var
                ))
            }
        }
    }
}

/// Helper function to parse provider string to LLMBackend
fn parse_provider(provider: &str) -> Result<LLMBackend, String> {
    match provider.to_lowercase().as_str() {
        "ollama" => Ok(LLMBackend::Ollama),
        "anthropic" | "claude" => Ok(LLMBackend::Anthropic),
        "openai" | "gpt" => Ok(LLMBackend::OpenAI),
        "deepseek" => Ok(LLMBackend::DeepSeek),
        "xai" | "x.ai" => Ok(LLMBackend::XAI),
        "phind" => Ok(LLMBackend::Phind),
        "google" | "gemini" => Ok(LLMBackend::Google),
        "groq" => Ok(LLMBackend::Groq),
        "azure" | "azureopenai" | "azure-openai" => Ok(LLMBackend::AzureOpenAI),
        "elevenlabs" | "11labs" => Ok(LLMBackend::ElevenLabs),
        "cohere" => Ok(LLMBackend::Cohere),
        "mistral" => Ok(LLMBackend::Mistral),
        "openrouter" => Ok(LLMBackend::OpenRouter),
        _ => Err(format!("Unknown provider: {}", provider)),
    }
}

/// Helper function to build LLM from config
fn build_llm_from_config(
    config: &LLMConfig,
    backend: LLMBackend,
) -> Result<Box<dyn LLMProvider>, String> {
    let mut builder = LLMBuilder::new().backend(backend.clone());

    // Parse model name from "provider::model" format
    let model_name = if config.model.contains("::") {
        config.model.split("::").nth(1).unwrap_or(&config.model)
    } else {
        &config.model
    };

    builder = builder.model(model_name);

    // Apply all configuration options
    if let Some(max_tokens) = config.max_tokens {
        builder = builder.max_tokens(max_tokens);
    }

    if let Some(ref api_key) = config.api_key {
        builder = builder.api_key(api_key);
    }

    if let Some(ref base_url) = config.base_url {
        if !base_url.is_empty() {
            builder = builder.base_url(base_url);
        }
    }

    if let Some(temperature) = config.temperature {
        builder = builder.temperature(temperature);
    }

    if let Some(top_p) = config.top_p {
        builder = builder.top_p(top_p);
    }

    if let Some(top_k) = config.top_k {
        builder = builder.top_k(top_k);
    }

    if let Some(ref system) = config.system {
        builder = builder.system(system);
    }

    if let Some(timeout) = config.timeout_seconds {
        builder = builder.timeout_seconds(timeout);
    }

    if let Some(ref format) = config.embedding_encoding_format {
        builder = builder.embedding_encoding_format(format);
    }

    if let Some(dims) = config.embedding_dimensions {
        builder = builder.embedding_dimensions(dims);
    }

    if let Some(enabled) = config.enable_parallel_tool_use {
        builder = builder.enable_parallel_tool_use(enabled);
    }

    if let Some(enabled) = config.reasoning {
        builder = builder.reasoning(enabled);
    }

    if let Some(budget) = config.reasoning_budget_tokens {
        builder = builder.reasoning_budget_tokens(budget);
    }

    // Azure-specific
    if let Some(ref api_version) = config.api_version {
        builder = builder.api_version(api_version);
    }

    if let Some(ref deployment_id) = config.deployment_id {
        builder = builder.deployment_id(deployment_id);
    }

    // Voice
    if let Some(ref voice) = config.voice {
        builder = builder.voice(voice);
    }

    // XAI search parameters
    if let Some(ref mode) = config.xai_search_mode {
        builder = builder.xai_search_mode(mode);
    }

    // XAI search source uses a combined method
    if let (Some(source_type), excluded) = (
        &config.xai_search_source_type,
        &config.xai_search_excluded_websites,
    ) {
        builder = builder.xai_search_source(source_type, excluded.clone());
    }

    if let Some(ref from_date) = config.xai_search_from_date {
        builder = builder.xai_search_from_date(from_date);
    }

    if let Some(ref to_date) = config.xai_search_to_date {
        builder = builder.xai_search_to_date(to_date);
    }

    // OpenAI web search
    if let Some(enabled) = config.openai_enable_web_search {
        builder = builder.openai_enable_web_search(enabled);
    }

    if let Some(ref context_size) = config.openai_web_search_context_size {
        builder = builder.openai_web_search_context_size(context_size);
    }

    if let Some(ref loc_type) = config.openai_web_search_user_location_type {
        builder = builder.openai_web_search_user_location_type(loc_type);
    }

    if let Some(ref country) = config.openai_web_search_user_location_approximate_country {
        builder = builder.openai_web_search_user_location_approximate_country(country);
    }

    if let Some(ref city) = config.openai_web_search_user_location_approximate_city {
        builder = builder.openai_web_search_user_location_approximate_city(city);
    }

    if let Some(ref region) = config.openai_web_search_user_location_approximate_region {
        builder = builder.openai_web_search_user_location_approximate_region(region);
    }

    // Resilience
    if let Some(enabled) = config.resilient_enable {
        builder = builder.resilient(enabled);
    }

    if let Some(attempts) = config.resilient_attempts {
        builder = builder.resilient_attempts(attempts);
    }

    builder
        .build()
        .map_err(|e| format!("Failed to build LLM: {}", e))
}

/// Estimate token count based on text length (~4 chars per token)
fn estimate_tokens(text: &str) -> u64 {
    ((text.len() as f64) / 4.0).ceil() as u64
}

/// Get model pricing in micro-dollars per 1K tokens (input, output)
fn get_model_pricing(model: &str) -> (u64, u64) {
    match model.to_lowercase().as_str() {
        m if m.contains("gpt-4o") => (2_500, 10_000),
        m if m.contains("gpt-4-turbo") => (10_000, 30_000),
        m if m.contains("gpt-4") => (30_000, 60_000),
        m if m.contains("gpt-3.5-turbo") => (500, 1_500),
        m if m.contains("claude-3-opus") => (15_000, 75_000),
        m if m.contains("claude-3-5-sonnet") => (3_000, 15_000),
        m if m.contains("claude-3-sonnet") => (3_000, 15_000),
        m if m.contains("claude-3-haiku") => (250, 1_250),
        _ => (500, 1_500),
    }
}

/// Calculate cost in micro-dollars
fn calculate_cost(model: &str, input_tokens: u64, output_tokens: u64) -> u64 {
    let (input_price, output_price) = get_model_pricing(model);
    (input_tokens * input_price + output_tokens * output_price) / 1000
}

pub struct UniversalLLMClient {
    config: LLMProviderConfig,
    llm: Box<dyn LLMProvider>,
}

#[async_trait]
pub trait LLMClient: Send + Sync {
    /// Send messages to LLM and get a response
    async fn complete<T, C>(&self, messages: &[Message], tools: &[ToolSpec]) -> Result<T, String>
    where
        T: LLMResponseTrait<C> + Default + Send,
        C: for<'de> Deserialize<'de> + Default + Send + Serialize;
}

impl Clone for UniversalLLMClient {
    fn clone(&self) -> Self {
        let config = self.config.clone();
        let model = config.clone().model;
        let api_key = config.api_key.clone();
        let base_url = config.base_url.clone();
        let parts: Vec<&str> = model.split("::").collect();

        let provider = parts[0];
        let model = parts[1];

        let backend = parse_provider(provider).unwrap_or(LLMBackend::Ollama);

        let mut builder = LLMBuilder::new()
            .backend(backend.clone())
            .model(model)
            .max_tokens(4096);

        if let Some(api_key) = api_key {
            builder = builder.api_key(api_key);
        }

        if !base_url.is_empty() {
            builder = builder.base_url(base_url);
        }

        let llm = builder
            .build()
            .map_err(|e| format!("Failed to build LLM: {}", e))
            .unwrap();

        Self {
            llm,
            config: config.clone(),
        }
    }
}

impl UniversalLLMClient {
    const DEFAULT_SYSTEM_PROMPT: &'static str = "You are a helpful AI assistant.";

    // Updated: Now supports multiple tool calls
    const DEFAULT_TOOL_PROMPT: &'static str = "You have access to the following tools.\n\
         To call ONE tool, respond EXACTLY in this format:\n\
         USE_TOOL: tool_name\n\
         {\"param1\": \"value1\"}\n\n\
         To call MULTIPLE tools at once, respond in this format:\n\
         USE_TOOLS:\n\
         tool_name1\n\
         {\"param1\": \"value1\"}\n\
         ---\n\
         tool_name2\n\
         {\"param1\": \"value1\"}\n\n\
         Only call tools using these exact formats. Otherwise, respond normally.";

    fn generate_schema_instruction<C>(sample: &C) -> String
    where
        C: Serialize,
    {
        let sample_json = serde_json::to_string_pretty(sample).unwrap_or_else(|_| "{}".to_string());

        format!(
            "Respond with ONLY a JSON object in this exact format:\n{}\n\nProvide your response as valid JSON.",
            sample_json
        )
    }

    pub fn new(provider_model: &str, api_key: Option<String>) -> Result<Self, String> {
        let parts: Vec<&str> = provider_model.split("::").collect();

        if parts.len() != 2 {
            return Err(format!(
                "Invalid format. Use 'provider::model-name'. Got: {}",
                provider_model
            ));
        }

        let provider = parts[0];
        let model = parts[1];

        // Determine the API key to use: provided > environment variable > error if required
        let final_api_key = match api_key {
            Some(key) => Some(key),
            None => {
                // Try to get from environment variable
                match get_api_key_from_env(provider) {
                    Ok(env_key) => env_key,
                    Err(e) => return Err(e), // Required but not found
                }
            }
        };

        let config = LLMProviderConfig {
            model: provider_model.to_string(),
            max_tokens: 4096,
            api_key: final_api_key.clone(),
            base_url: String::new(),
        };

        let backend = parse_provider(provider)?;

        let base_url = match provider.to_lowercase().as_str() {
            "ollama" => std::env::var("OLLAMA_URL").unwrap_or("http://127.0.0.1:11434".to_string()),
            _ => String::new(),
        };

        let mut builder = LLMBuilder::new()
            .backend(backend.clone())
            .model(model)
            .max_tokens(4096);

        if let Some(api_key) = final_api_key {
            builder = builder.api_key(api_key);
        }

        if !base_url.is_empty() {
            builder = builder.base_url(base_url);
        }

        let llm = builder
            .build()
            .map_err(|e| format!("Failed to build LLM: {}", e))?;

        Ok(Self { llm, config })
    }

    /// Create a new UniversalLLMClient with comprehensive LLMConfig
    ///
    /// # Examples
    ///
    /// ```rust,no_run
    /// use runtime::llm::LLMConfig;
    /// use runtime::llm::UniversalLLMClient;
    ///
    /// let config = LLMConfig::new("openai::gpt-4")
    ///     .with_api_key("your-api-key")
    ///     .with_temperature(0.7)
    ///     .with_max_tokens(2048);
    ///
    /// let client = UniversalLLMClient::new_with_config(config).unwrap();
    /// ```
    pub fn new_with_config(llm_config: LLMConfig) -> Result<Self, String> {
        // Parse provider from model string
        let parts: Vec<&str> = llm_config.model.split("::").collect();

        if parts.len() != 2 {
            return Err(format!(
                "Invalid format. Use 'provider::model-name'. Got: {}",
                llm_config.model
            ));
        }

        let provider = parts[0];
        let backend = parse_provider(provider)?;

        // Set default base_url for certain providers if not specified
        let mut config = llm_config.clone();
        if config.base_url.is_none() {
            match provider.to_lowercase().as_str() {
                "ollama" => {
                    config.base_url = Some(
                        std::env::var("OLLAMA_URL").unwrap_or("http://127.0.0.1:11434".to_string()),
                    );
                }
                _ => {}
            }
        }

        // Check for API key: provided > environment variable > error if required
        if config.api_key.is_none() {
            match get_api_key_from_env(provider) {
                Ok(env_key) => config.api_key = env_key,
                Err(e) => return Err(e), // Required but not found
            }
        }

        // Build LLM using the comprehensive config
        let llm = build_llm_from_config(&config, backend)?;

        // Convert to legacy config for internal storage
        let legacy_config = LLMProviderConfig::from(config);

        Ok(Self {
            llm,
            config: legacy_config,
        })
    }

    fn convert_messages(&self, messages: &[Message]) -> Vec<ChatMessage> {
        messages
            .iter()
            .map(|msg| match msg.role.as_str() {
                "user" => ChatMessage::user().content(&msg.content).build(),
                "assistant" => ChatMessage::assistant().content(&msg.content).build(),
                "system" => ChatMessage::assistant().content(&msg.content).build(),
                "tool" => ChatMessage::assistant()
                    .content(format!("Tool result: {}", msg.content))
                    .build(),
                _ => ChatMessage::user().content(&msg.content).build(),
            })
            .collect()
    }

    fn build_tool_description(tools: &[ToolSpec]) -> String {
        tools
            .iter()
            .map(|t| {
                let params = t
                    .input_schema
                    .get("properties")
                    .and_then(|p| p.as_object())
                    .map(|o| o.keys().cloned().collect::<Vec<_>>().join(", "))
                    .unwrap_or_default();

                if t.description.is_empty() {
                    format!("- {}({})", t.name, params)
                } else {
                    format!("- {}({}): {}", t.name, params, t.description)
                }
            })
            .collect::<Vec<_>>()
            .join("\n")
    }

    // New helper: Parse multiple tool calls from response
    fn parse_tool_calls(response_text: &str) -> Vec<ToolCall> {
        let mut tool_calls = Vec::new();

        // Check for multiple tools format
        if response_text.starts_with("USE_TOOLS:") {
            // Split by "---" to get individual tool calls
            let parts: Vec<&str> = response_text
                .strip_prefix("USE_TOOLS:")
                .unwrap_or("")
                .split("---")
                .collect();

            for part in parts {
                let lines: Vec<&str> = part.trim().lines().collect();
                if lines.is_empty() {
                    continue;
                }

                let tool_name = lines[0].trim().to_string();
                let json_block = lines.get(1..).unwrap_or(&[]).join("\n");

                if let Ok(input_value) = serde_json::from_str(&json_block) {
                    tool_calls.push(ToolCall {
                        name: tool_name,
                        input: input_value,
                    });
                }
            }
        }
        // Check for single tool format
        else if response_text.starts_with("USE_TOOL:") {
            let lines: Vec<&str> = response_text.lines().collect();
            let tool_name = lines[0]
                .strip_prefix("USE_TOOL:")
                .unwrap_or("")
                .trim()
                .to_string();

            let json_block = lines.get(1..).unwrap_or(&[]).join("\n");

            if let Ok(input_value) = serde_json::from_str(&json_block) {
                tool_calls.push(ToolCall {
                    name: tool_name,
                    input: input_value,
                });
            }
        }

        tool_calls
    }
}

#[async_trait]
impl LLMClient for UniversalLLMClient {
    async fn complete<T, C>(&self, messages: &[Message], tools: &[ToolSpec]) -> Result<T, String>
    where
        T: LLMResponseTrait<C> + Default + Send,
        C: for<'de> Deserialize<'de> + Default + Send + Serialize,
    {
        let mut chat_messages = vec![];

        // 1) Add system prompt if not provided by user
        let has_user_system_prompt = messages.iter().any(|m| m.role == "system");
        if !has_user_system_prompt {
            chat_messages.push(
                ChatMessage::assistant()
                    .content(Self::DEFAULT_SYSTEM_PROMPT)
                    .build(),
            );
        }

        // 2) Add tool prompt if tools are provided
        let user_tool_prompt = messages
            .iter()
            .find(|m| m.role == "system_tools")
            .map(|m| m.content.clone());

        if !tools.is_empty() {
            let tool_list = Self::build_tool_description(tools);
            let tool_prompt = user_tool_prompt.unwrap_or_else(|| {
                format!(
                    "{}\n\nAvailable Tools:\n{}\n\n{}",
                    Self::DEFAULT_TOOL_PROMPT,
                    tool_list,
                    "Use only the EXACT formats shown above when calling tools."
                )
            });
            chat_messages.push(ChatMessage::assistant().content(tool_prompt).build());
        }

        // 3) AUTO-GENERATE SCHEMA INSTRUCTION
        let sample_c = C::default();
        let schema_instruction = Self::generate_schema_instruction(&sample_c);

        chat_messages.push(ChatMessage::assistant().content(schema_instruction).build());

        // 4) Add user messages
        chat_messages.extend(self.convert_messages(messages));

        // Helper: try to parse into C
        let try_parse_c = |s: &str| -> C {
            let text = s.trim();

            // Try direct JSON parse
            if let Ok(parsed) = serde_json::from_str::<C>(text) {
                return parsed;
            }

            // Remove markdown code blocks
            let cleaned = text
                .strip_prefix("```json")
                .unwrap_or(text)
                .strip_prefix("```")
                .unwrap_or(text)
                .strip_suffix("```")
                .unwrap_or(text)
                .trim();

            if let Ok(parsed) = serde_json::from_str::<C>(cleaned) {
                return parsed;
            }

            // Find JSON object in text
            if let Some(start) = text.find('{') {
                if let Some(end) = text.rfind('}') {
                    let json_part = &text[start..=end];
                    if let Ok(parsed) = serde_json::from_str::<C>(json_part) {
                        return parsed;
                    }
                }
            }

            // Try quoted string
            if let Ok(quoted) = serde_json::to_string(text) {
                if let Ok(parsed) = serde_json::from_str::<C>(&quoted) {
                    return parsed;
                }
            }

            // Fallback to default
            C::default()
        };

        // 5) Send to LLM
        let start = std::time::Instant::now();
        let response = self
            .llm
            .chat(&chat_messages)
            .await
            .map_err(|e| format!("LLM error: {}", e))?;
        let duration = start.elapsed().as_micros() as u64;

        let response_text = response.text().unwrap_or_default();

        // Estimate tokens and cost
        let input_text: String = messages
            .iter()
            .map(|m| m.content.as_str())
            .collect::<Vec<_>>()
            .join(" ");
        let input_tokens = estimate_tokens(&input_text);
        let output_tokens = estimate_tokens(&response_text);
        let total_tokens = input_tokens + output_tokens;
        let cost_us = calculate_cost(&self.config.model, input_tokens, output_tokens);

        // Record metrics with estimates
        crate::metrics::metrics().record_llm_call(duration, total_tokens, cost_us);

        // 6) Parse tool calls (handles both single and multiple)
        let tool_calls = Self::parse_tool_calls(&response_text);

        // If we have tool calls, return them
        if !tool_calls.is_empty() {
            let parsed_content: C = C::default();
            return Ok(T::new(parsed_content, tool_calls, false));
        }

        // 7) Normal response - parse into C
        let parsed_content: C = try_parse_c(&response_text);
        Ok(T::new(parsed_content, vec![], true))
    }
}

// ============================================================================
// MOCK LLM CLIENT FOR TESTING
// ============================================================================

/// Mock LLM client for testing - doesn't make real API calls.
///
/// This is useful for writing fast unit tests without requiring actual LLM API access.
///
/// # Examples
///
/// ```rust
/// use runtime::llm::{MockLLMClient, LLMClient, LLMResponse};
/// use runtime::llm::types::Message;
///
/// # #[tokio::main]
/// # async fn main() {
/// let client = MockLLMClient::new("Hello from mock!");
/// let messages = vec![Message {
///     role: "user".to_string(),
///     content: "Say hello".to_string(),
/// }];
///
/// let result: LLMResponse<String> = client
///     .complete::<LLMResponse<String>, String>(&messages, &[])
///     .await
///     .expect("Mock LLM failed");
/// # }
/// ```
pub struct MockLLMClient {
    response_content: String,
}

impl MockLLMClient {
    /// Creates a new mock LLM client that returns the specified response.
    ///
    /// # Arguments
    ///
    /// * `response` - A string that will be parsed as the response content
    ///
    /// # Examples
    ///
    /// ```rust
    /// use runtime::llm::MockLLMClient;
    ///
    /// // For structured responses, provide JSON
    /// let client = MockLLMClient::new(r#"{"field": "value"}"#);
    ///
    /// // For simple text responses
    /// let client = MockLLMClient::new("Hello, world!");
    /// ```
    pub fn new(response: &str) -> Self {
        Self {
            response_content: response.to_string(),
        }
    }

    /// Creates a mock LLM client with a default "Hello" response.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use runtime::llm::MockLLMClient;
    ///
    /// let client = MockLLMClient::default_hello();
    /// ```
    pub fn default_hello() -> Self {
        Self::new("Hello! How can I help you today?")
    }
}

#[async_trait::async_trait]
impl LLMClient for MockLLMClient {
    async fn complete<T, C>(&self, _messages: &[Message], _tools: &[ToolSpec]) -> Result<T, String>
    where
        T: LLMResponseTrait<C> + Default + Send,
        C: for<'de> Deserialize<'de> + Default + Send + Serialize,
    {
        // Try to parse the response into the expected content type
        let content: C = if let Ok(parsed) = serde_json::from_str(&self.response_content) {
            parsed
        } else {
            C::default()
        };

        Ok(T::new(content, vec![], true))
    }
}

// ============================================================================
// TESTS
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_mock_llm_basic() {
        let client = MockLLMClient::default_hello();
        let messages = vec![Message {
            role: "user".into(),
            content: "Say hello".into(),
        }];

        let result: LLMResponse<String> = client
            .complete::<LLMResponse<String>, String>(&messages, &[])
            .await
            .expect("Mock LLM failed");

        assert!(result.content.is_empty()); // Default String is empty
        assert!(result.tool_calls.is_empty());
        assert!(result.is_complete);
    }

    #[tokio::test]
    async fn test_mock_structured_output() {
        let client = MockLLMClient::new(r#"{"field1": 42.5, "flag": true}"#);
        let messages = vec![Message {
            role: "user".into(),
            content: "Return structured data".into(),
        }];

        #[derive(Deserialize, Serialize, Default, Clone, Debug)]
        struct MyOutput {
            field1: f64,
            flag: bool,
        }

        let result: LLMResponse<MyOutput> = client
            .complete::<LLMResponse<MyOutput>, MyOutput>(&messages, &[])
            .await
            .expect("Mock LLM failed");

        assert_eq!(result.content.field1, 42.5);
        assert_eq!(result.content.flag, true);
        assert!(result.tool_calls.is_empty());
        assert!(result.is_complete);
    }
}
