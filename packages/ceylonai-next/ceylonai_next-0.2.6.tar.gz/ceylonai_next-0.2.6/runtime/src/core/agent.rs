use crate::core::error::Result;
use crate::core::message::Message;
use async_trait::async_trait;

#[async_trait]
pub trait Agent: Send + Sync {
    fn name(&self) -> String;
    async fn on_start(&mut self, _ctx: &mut AgentContext) -> Result<()> {
        Ok(())
    }
    async fn on_message(&mut self, _msg: Message, _ctx: &mut AgentContext) -> Result<()> {
        // Default implementation does nothing
        Ok(())
    }

    /// Handle a generic string message and return a generic response.
    /// Default implementation returns an echo response.
    async fn on_generic_message(
        &mut self,
        msg: crate::core::message::GenericMessage,
        _ctx: &mut AgentContext,
    ) -> Result<crate::core::message::GenericResponse> {
        // Simple default: echo the content back
        Ok(crate::core::message::GenericResponse::new(msg.content))
    }
    async fn on_stop(&mut self, _ctx: &mut AgentContext) -> Result<()> {
        Ok(())
    }

    /// Get the tool invoker for this agent (if it has actions)
    fn tool_invoker(&self) -> Option<&crate::core::action::ToolInvoker> {
        None // Default: no actions
    }

    /// Get mutable tool invoker for registration
    fn tool_invoker_mut(&mut self) -> Option<&mut crate::core::action::ToolInvoker> {
        None
    }
}

pub struct AgentContext {
    pub mesh_name: String,
    // We will add methods here to send messages back to the mesh
    // For now, it's a placeholder to pass context
}

impl AgentContext {
    pub fn new(mesh_name: String) -> Self {
        Self { mesh_name }
    }
}
