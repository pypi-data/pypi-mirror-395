use crate::ceylon;
use runtime::core::message::Message;
use std::collections::HashMap;

impl From<ceylon::Message> for Message {
    fn from(msg: ceylon::Message) -> Self {
        Message {
            id: msg.id,
            topic: msg.topic,
            payload: msg.payload.to_vec(),
            sender: msg.sender,
            metadata: msg.metadata,
            created_at: chrono::Utc::now().timestamp_micros(),
        }
    }
}

impl From<Message> for ceylon::Message {
    fn from(msg: Message) -> Self {
        ceylon::Message {
            id: msg.id,
            topic: msg.topic,
            payload: msg.payload.into(),
            sender: msg.sender,
            metadata: msg.metadata,
        }
    }
}
