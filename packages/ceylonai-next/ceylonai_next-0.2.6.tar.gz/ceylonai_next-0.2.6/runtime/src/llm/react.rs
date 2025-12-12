use crate::core::action::ToolInvoker;
use crate::core::agent::AgentContext;
use crate::core::error::Result;
use crate::core::memory::Memory;
use crate::llm::types::Message;
use crate::llm::{LLMClient, LLMConfig, LLMResponse, UniversalLLMClient};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::Mutex;

/// Configuration for ReAct (Reason + Act) mode.
///
/// ReAct enables agents to perform autonomous reasoning and action execution
/// in an interleaved loop, alternating between thoughts and actions.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReActConfig {
    /// Whether ReAct mode is enabled
    pub enabled: bool,

    /// Maximum number of reasoning iterations
    pub max_iterations: usize,

    /// Prefix for thought traces (default: "Thought:")
    pub thought_prefix: String,

    /// Prefix for actions (default: "Action:")
    pub action_prefix: String,

    /// Prefix for observations (default: "Observation:")
    pub observation_prefix: String,

    /// Name of the finish action (default: "finish")
    pub finish_action: String,

    /// Stop sequences for LLM generation
    pub stop_sequences: Vec<String>,
}

impl Default for ReActConfig {
    fn default() -> Self {
        Self {
            enabled: false,
            max_iterations: 10,
            thought_prefix: "Thought:".to_string(),
            action_prefix: "Action:".to_string(),
            observation_prefix: "Observation:".to_string(),
            finish_action: "finish".to_string(),
            stop_sequences: vec!["Observation:".to_string()],
        }
    }
}

impl ReActConfig {
    /// Create a new ReActConfig with default settings
    pub fn new() -> Self {
        Self::default()
    }

    /// Enable ReAct mode
    pub fn enabled(mut self) -> Self {
        self.enabled = true;
        self
    }

    /// Set maximum iterations
    pub fn with_max_iterations(mut self, max_iterations: usize) -> Self {
        self.max_iterations = max_iterations;
        self
    }

    /// Set thought prefix
    pub fn with_thought_prefix(mut self, prefix: impl Into<String>) -> Self {
        self.thought_prefix = prefix.into();
        self
    }

    /// Set action prefix
    pub fn with_action_prefix(mut self, prefix: impl Into<String>) -> Self {
        self.action_prefix = prefix.into();
        self
    }

    /// Set observation prefix
    pub fn with_observation_prefix(mut self, prefix: impl Into<String>) -> Self {
        self.observation_prefix = prefix.into();
        self
    }
}

/// A single step in the ReAct reasoning process.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReActStep {
    /// Iteration number (1-indexed)
    pub iteration: usize,

    /// The agent's reasoning/thought
    pub thought: String,

    /// The action name (if any)
    pub action: Option<String>,

    /// The action input (if any)
    pub action_input: Option<String>,

    /// The observation from executing the action
    pub observation: Option<String>,
}

/// Result of a ReAct reasoning process.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReActResult {
    /// The final answer
    pub answer: String,

    /// All reasoning steps taken
    pub steps: Vec<ReActStep>,

    /// Number of iterations performed
    pub iterations: usize,

    /// Reason for finishing
    pub finish_reason: FinishReason,
}

/// Reason why ReAct finished.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum FinishReason {
    /// The finish action was called successfully
    Success,

    /// Maximum iterations reached
    MaxIterations,

    /// An error occurred
    Error(String),
}

/// ReAct engine for executing the reasoning loop.
pub struct ReActEngine {
    config: ReActConfig,
    tool_invoker: Option<Arc<Mutex<ToolInvoker>>>,
}

impl ReActEngine {
    /// Create a new ReAct engine
    pub fn new(config: ReActConfig, tool_invoker: Option<Arc<Mutex<ToolInvoker>>>) -> Self {
        Self {
            config,
            tool_invoker,
        }
    }

    /// Execute the ReAct loop
    pub async fn execute(
        &self,
        query: String,
        llm_client: &UniversalLLMClient,
        _llm_config: &LLMConfig,
        _memory: Option<&Arc<dyn Memory>>,
        ctx: &mut AgentContext,
    ) -> Result<ReActResult> {
        let mut steps = Vec::new();
        let mut conversation_history = self.build_initial_messages(&query);

        for iteration in 1..=self.config.max_iterations {
            // Build prompt for this iteration
            let prompt = self.build_iteration_prompt(&query, &steps);

            // Add to conversation
            conversation_history.push(Message {
                role: "user".to_string(),
                content: prompt,
            });

            // Call LLM
            let response: LLMResponse<String> = llm_client
                .complete::<LLMResponse<String>, String>(&conversation_history, &[])
                .await
                .map_err(|e| crate::core::error::Error::MeshError(e))?;

            // Parse the LLM output
            let step = self.parse_step(iteration, &response.content)?;

            // Check if this is the finish action
            if let Some(ref action_name) = step.action {
                if action_name == &self.config.finish_action {
                    // Extract the final answer from action_input
                    let answer = step
                        .action_input
                        .clone()
                        .unwrap_or_else(|| step.thought.clone());

                    steps.push(step);

                    return Ok(ReActResult {
                        answer,
                        steps,
                        iterations: iteration,
                        finish_reason: FinishReason::Success,
                    });
                }
            }

            // Execute action if present
            let mut step_with_observation = step.clone();

            if let (Some(ref action_name), Some(ref action_input)) =
                (&step.action, &step.action_input)
            {
                let observation = self.execute_action(action_name, action_input, ctx).await?;
                step_with_observation.observation = Some(observation.clone());

                // Add observation to conversation
                conversation_history.push(Message {
                    role: "assistant".to_string(),
                    content: response.content.clone(),
                });

                conversation_history.push(Message {
                    role: "user".to_string(),
                    content: format!("{} {}", self.config.observation_prefix, observation),
                });
            } else {
                // No action, just add the thought
                conversation_history.push(Message {
                    role: "assistant".to_string(),
                    content: response.content,
                });
            }

            steps.push(step_with_observation);
        }

        // Max iterations reached
        let last_thought = steps.last().map(|s| s.thought.clone()).unwrap_or_default();

        Ok(ReActResult {
            answer: last_thought,
            steps,
            iterations: self.config.max_iterations,
            finish_reason: FinishReason::MaxIterations,
        })
    }

    /// Build initial system messages  
    fn build_initial_messages(&self, _query: &str) -> Vec<Message> {
        let system_prompt = self.build_react_system_prompt();

        vec![Message {
            role: "system".to_string(),
            content: system_prompt,
        }]
    }

    /// Build the ReAct system prompt
    fn build_react_system_prompt(&self) -> String {
        format!(
            "You are a ReAct (Reason + Act) agent. You solve problems by alternating between reasoning and taking actions.\n\n\
            On each turn, you must:\n\
            1. Output your reasoning prefixed with '{}'\n\
            2. Decide on an action prefixed with '{}'\n\
            3. Wait for an observation prefixed with '{}'\n\n\
            Format:\n\
            {} [your reasoning about the problem]\n\
            {} action_name[action_input]\n\n\
            Example:\n\
            {} I need to find information about X\n\
            {} search[X]\n\n\
            When you have the final answer, use:\n\
            {} {}[your final answer]\n\n\
            Available actions will be provided with each query.",
            self.config.thought_prefix,
            self.config.action_prefix,
            self.config.observation_prefix,
            self.config.thought_prefix,
            self.config.action_prefix,
            self.config.thought_prefix,
            self.config.action_prefix,
            self.config.action_prefix,
            self.config.finish_action
        )
    }

    /// Build prompt for current iteration
    fn build_iteration_prompt(&self, query: &str, steps: &[ReActStep]) -> String {
        if steps.is_empty() {
            // First iteration
            format!("Question: {}\n\nBegin reasoning:", query)
        } else {
            // Continue from previous step
            "Continue reasoning:".to_string()
        }
    }

    /// Parse LLM output into a ReActStep
    fn parse_step(&self, iteration: usize, output: &str) -> Result<ReActStep> {
        let mut thought = String::new();
        let mut action: Option<String> = None;
        let mut action_input: Option<String> = None;

        // Parse line by line
        for line in output.lines() {
            let line = line.trim();

            if line.starts_with(&self.config.thought_prefix) {
                thought = line
                    .strip_prefix(&self.config.thought_prefix)
                    .unwrap_or("")
                    .trim()
                    .to_string();
            } else if line.starts_with(&self.config.action_prefix) {
                // Parse Action: action_name[input]
                let action_str = line
                    .strip_prefix(&self.config.action_prefix)
                    .unwrap_or("")
                    .trim();

                if let Some(bracket_pos) = action_str.find('[') {
                    let name = action_str[..bracket_pos].trim().to_string();
                    let input = action_str[bracket_pos + 1..]
                        .trim_end_matches(']')
                        .trim()
                        .to_string();

                    action = Some(name);
                    action_input = Some(input);
                } else {
                    // No brackets, entire string is action name
                    action = Some(action_str.to_string());
                }
            }
        }

        Ok(ReActStep {
            iteration,
            thought,
            action,
            action_input,
            observation: None,
        })
    }

    /// Execute an action using the tool invoker
    async fn execute_action(
        &self,
        action_name: &str,
        action_input: &str,
        ctx: &mut AgentContext,
    ) -> Result<String> {
        if let Some(ref tool_invoker) = self.tool_invoker {
            let invoker = tool_invoker.lock().await;

            // Convert string input to JSON value
            let input_value: serde_json::Value = serde_json::from_str(action_input)
                .unwrap_or_else(|_| serde_json::json!({"input": action_input}));

            let result = invoker.invoke(action_name, ctx, input_value).await?;

            Ok(result.to_string())
        } else {
            Ok(format!(
                "No tool invoker available to execute action: {}",
                action_name
            ))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_react_config_default() {
        let config = ReActConfig::default();
        assert_eq!(config.enabled, false);
        assert_eq!(config.max_iterations, 10);
        assert_eq!(config.thought_prefix, "Thought:");
        assert_eq!(config.action_prefix, "Action:");
    }

    #[test]
    fn test_react_config_builder() {
        let config = ReActConfig::new()
            .enabled()
            .with_max_iterations(15)
            .with_thought_prefix("Think:");

        assert_eq!(config.enabled, true);
        assert_eq!(config.max_iterations, 15);
        assert_eq!(config.thought_prefix, "Think:");
    }

    #[test]
    fn test_parse_step() {
        let config = ReActConfig::default();
        let engine = ReActEngine::new(config, None);

        let output = "Thought: I need to search for information\nAction: search[test query]";
        let step = engine.parse_step(1, output).unwrap();

        assert_eq!(step.iteration, 1);
        assert_eq!(step.thought, "I need to search for information");
        assert_eq!(step.action, Some("search".to_string()));
        assert_eq!(step.action_input, Some("test query".to_string()));
    }
}
