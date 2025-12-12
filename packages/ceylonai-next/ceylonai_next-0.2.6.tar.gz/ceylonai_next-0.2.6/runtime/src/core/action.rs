use crate::core::agent::AgentContext;
use crate::core::error::Result;
use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

/// Metadata describing an action
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActionMetadata {
    /// Action name (unique within an agent)
    pub name: String,

    /// Human-readable description
    pub description: String,

    /// JSON Schema for input validation
    pub input_schema: Value,

    /// JSON Schema for output (optional)
    pub output_schema: Option<Value>,
}

/// Trait for invoking actions with context
#[async_trait]
pub trait ActionInvoker: Send + Sync {
    /// Execute the action with given context and inputs
    async fn execute(&self, ctx: &mut AgentContext, inputs: Value) -> Result<Value>;

    /// Get action metadata
    fn metadata(&self) -> &ActionMetadata;
}

/// Manages action registration and execution for an agent
pub struct ToolInvoker {
    actions: HashMap<String, Box<dyn ActionInvoker>>,
}

impl ToolInvoker {
    /// Create a new ToolInvoker
    pub fn new() -> Self {
        Self {
            actions: HashMap::new(),
        }
    }

    /// Register an action
    pub fn register(&mut self, action: Box<dyn ActionInvoker>) {
        let name = action.metadata().name.clone();
        self.actions.insert(name, action);
    }

    /// List all registered actions
    pub fn list_actions(&self) -> Vec<ActionMetadata> {
        self.actions
            .values()
            .map(|a| a.metadata().clone())
            .collect()
    }

    /// Invoke an action by name
    pub async fn invoke(&self, name: &str, ctx: &mut AgentContext, inputs: Value) -> Result<Value> {
        let action = self
            .actions
            .get(name)
            .ok_or_else(|| crate::core::error::Error::ActionNotFound(name.to_string()))?;

        action.execute(ctx, inputs).await
    }
}

impl Default for ToolInvoker {
    fn default() -> Self {
        Self::new()
    }
}
