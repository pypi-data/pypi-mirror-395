#[cfg(test)]
mod tests {
    use async_trait::async_trait;
    use runtime::core::action::{ActionInvoker, ActionMetadata, ToolInvoker};
    use runtime::core::agent::{Agent, AgentContext};
    use runtime::core::error::Result;
    use runtime::core::mesh::Mesh;
    use runtime::core::message::Message;
    use runtime::local::LocalMesh;
    use serde_json::{json, Value};
    use std::sync::Arc;
    use tokio::sync::Mutex;

    struct PingAgent {
        received_pong: Arc<Mutex<bool>>,
    }

    #[async_trait]
    impl Agent for PingAgent {
        fn name(&self) -> String {
            "ping".to_string()
        }

        async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
            if msg.topic == "pong" {
                let mut lock = self.received_pong.lock().await;
                *lock = true;
            }
            Ok(())
        }
    }

    struct PongAgent {
        mesh: Arc<LocalMesh>,
    }

    #[async_trait]
    impl Agent for PongAgent {
        fn name(&self) -> String {
            "pong".to_string()
        }

        async fn on_message(&mut self, msg: Message, _ctx: &mut AgentContext) -> Result<()> {
            if msg.topic == "ping" {
                let response = Message::new("pong", vec![], "pong");
                self.mesh.send(response, "ping").await?;
            }
            Ok(())
        }
    }

    #[tokio::test]
    async fn test_ping_pong() {
        let mesh = Arc::new(LocalMesh::new("test-mesh"));
        let received_pong = Arc::new(Mutex::new(false));

        let ping_agent = PingAgent {
            received_pong: received_pong.clone(),
        };

        let pong_agent = PongAgent { mesh: mesh.clone() };

        mesh.add_agent(Box::new(ping_agent)).await.unwrap();
        mesh.add_agent(Box::new(pong_agent)).await.unwrap();

        let msg = Message::new("ping", vec![], "external");
        mesh.send(msg, "pong").await.unwrap();

        // Wait for processing
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

        let result = *received_pong.lock().await;
        assert!(result, "Ping agent should have received pong");
    }

    // Test action system
    struct TestActionInvoker {
        metadata: ActionMetadata,
    }

    #[async_trait]
    impl ActionInvoker for TestActionInvoker {
        async fn execute(&self, _ctx: &mut AgentContext, inputs: Value) -> Result<Value> {
            // Simple add action
            let a = inputs["a"].as_i64().unwrap_or(0);
            let b = inputs["b"].as_i64().unwrap_or(0);
            Ok(json!(a + b))
        }

        fn metadata(&self) -> &ActionMetadata {
            &self.metadata
        }
    }

    #[tokio::test]
    async fn test_action_system() {
        // Create action metadata
        let metadata = ActionMetadata {
            name: "add".to_string(),
            description: "Add two numbers".to_string(),
            input_schema: json!({
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }),
            output_schema: Some(json!({"type": "integer"})),
        };

        // Create tool invoker
        let mut tool_invoker = ToolInvoker::new();

        // Register action
        let action = Box::new(TestActionInvoker {
            metadata: metadata.clone(),
        });
        tool_invoker.register(action);

        // List actions
        let actions = tool_invoker.list_actions();
        assert_eq!(actions.len(), 1);
        assert_eq!(actions[0].name, "add");

        // Invoke action
        let mut ctx = AgentContext::new("test-mesh".to_string());
        let inputs = json!({"a": 5, "b": 3});
        let result = tool_invoker.invoke("add", &mut ctx, inputs).await.unwrap();

        assert_eq!(result, json!(8));
    }

    #[tokio::test]
    async fn test_action_not_found() {
        let tool_invoker = ToolInvoker::new();
        let mut ctx = AgentContext::new("test-mesh".to_string());
        let inputs = json!({});

        let result = tool_invoker.invoke("nonexistent", &mut ctx, inputs).await;
        assert!(result.is_err());

        if let Err(e) = result {
            assert!(e.to_string().contains("Action not found"));
        }
    }
}
