use distributed::ceylon::mesh_service_client::MeshServiceClient;
use distributed::ceylon::Envelope;
use runtime::Message;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Connect to the server
    let mut client = MeshServiceClient::connect("http://127.0.0.1:50051").await?;

    println!("Connected to server");

    // Create a message
    let msg = Message::new("test_topic", b"Hello from client!".to_vec(), "client_agent");

    // Convert to protobuf message (using the From implementation in distributed::conversion)
    // Note: We need to manually construct Envelope because we don't have a helper for it yet.
    // And we need to convert runtime::Message to ceylon::Message.
    // Since the From impl is in the library, we can use .into() if we import the trait or types correctly.
    // However, `distributed::ceylon::Message` is the proto type.

    let proto_msg: distributed::ceylon::Message = msg.into();

    let envelope = Envelope {
        message: Some(proto_msg),
        target_agent: Some("echo_agent".to_string()),
        target_node: None,
    };

    // Send the request
    let request = tonic::Request::new(envelope);
    let response = client.send(request).await?;

    println!("Response: {:?}", response.into_inner());

    Ok(())
}
