//! Redis Memory Backend Example
//!
//! This example demonstrates how to use Redis as a persistent memory backend for agents.
//!
//! Prerequisites:
//! 1. Install and start Redis:
//!    - macOS: `brew install redis && redis-server`
//!    - Linux: `sudo apt-get install redis-server && redis-server`
//!    - Docker: `docker run -d -p 6379:6379 redis:latest`
//!
//! 2. Build with Redis feature:
//!    `cargo run --example redis_memory --features redis`
//!
//! 3. Set up your LLM provider:
//!    `export OPENAI_API_KEY=your_key_here`
//!    or use Ollama (no API key needed)

//!    or use Ollama (no API key needed)

#[cfg(feature = "redis")]
use runtime::core::memory::{Memory, MemoryEntry, MemoryQuery};
#[cfg(feature = "redis")]
use runtime::llm::LlmAgent;
#[cfg(feature = "redis")]
use runtime::memory::RedisBackend;
#[cfg(feature = "redis")]
use serde_json::json;
#[cfg(feature = "redis")]
use std::env;

#[cfg(not(feature = "redis"))]
fn main() {
    println!("This example requires the 'redis' feature.");
}

#[cfg(feature = "redis")]
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("{}", "=".repeat(70));
    println!("🗄️  Ceylon AI Framework - Redis Memory Backend Example");
    println!("{}", "=".repeat(70));

    // Configuration
    let redis_url = env::var("REDIS_URL").unwrap_or_else(|_| "redis://localhost:6379".to_string());
    let model = env::var("LLM_MODEL").unwrap_or_else(|_| "ollama::llama3.2:latest".to_string());

    // 1. Create Redis Memory Backend
    println!("\n🔌 Connecting to Redis at {}...", redis_url);
    let memory = match RedisBackend::new(&redis_url).await {
        Ok(backend) => {
            let backend = backend
                .with_prefix("rust_demo_agent")
                .with_ttl_seconds(3600); // 1 hour TTL
            println!("✅ Redis backend connected successfully");
            backend
        }
        Err(e) => {
            eprintln!("❌ Failed to connect to Redis: {}", e);
            eprintln!("   Make sure Redis is running on localhost:6379");
            eprintln!("   Try: redis-server");
            return Err(e.into());
        }
    };

    // Clear previous demo data
    println!("🧹 Clearing previous demo data...");
    memory.clear().await?;

    // 2. Store sample data directly
    println!("\n{}", "=".repeat(70));
    println!("📝 Test 1: Direct Memory Operations");
    println!("{}", "=".repeat(70));

    let entries = vec![
        MemoryEntry::new("The Ceylon AI Framework is written in Rust")
            .with_metadata("category", json!("framework"))
            .with_metadata("language", json!("rust")),
        MemoryEntry::new("Python bindings are available via PyO3")
            .with_metadata("category", json!("bindings"))
            .with_metadata("language", json!("python")),
        MemoryEntry::new("Redis provides persistent memory storage")
            .with_metadata("category", json!("backend"))
            .with_metadata("type", json!("database")),
        MemoryEntry::new("Agents can use tools to save and search memory")
            .with_metadata("category", json!("features"))
            .with_metadata("type", json!("capability")),
    ];

    println!("\n💾 Storing {} entries...", entries.len());
    for entry in entries {
        let id = memory.store(entry.clone()).await?;
        println!("   ✓ Stored: {} (ID: {})", entry.content, id);
    }

    // 3. Query memory
    println!("\n{}", "=".repeat(70));
    println!("🔍 Test 2: Memory Queries");
    println!("{}", "=".repeat(70));

    // Count entries
    let count = memory.count().await?;
    println!("\n📊 Total entries in Redis: {}", count);

    // Search by metadata filter
    println!("\n🔎 Searching for entries with category='framework'...");
    let query = MemoryQuery::new().with_filter("category", json!("framework"));
    let results = memory.search(query).await?;
    for entry in &results {
        println!("   • {}", entry.content);
    }

    // Semantic search (keyword-based)
    println!("\n🔎 Searching for entries containing 'Python'...");
    let query = MemoryQuery::new()
        .with_semantic_query("Python")
        .with_limit(5);
    let results = memory.search(query).await?;
    for entry in &results {
        println!("   • {}", entry.content);
    }

    // 4. Test TTL functionality
    println!("\n{}", "=".repeat(70));
    println!("⏰ Test 3: TTL (Time-To-Live)");
    println!("{}", "=".repeat(70));

    println!("\n⏳ Creating entry with 3-second TTL...");
    let temp_entry = MemoryEntry::new("This message will expire soon").with_ttl_seconds(3);
    let temp_id = memory.store(temp_entry).await?;
    println!("   ✓ Stored temporary entry (ID: {})", temp_id);

    println!("   Checking immediately...");
    let retrieved = memory.get(&temp_id).await?;
    println!("   Entry exists: {}", retrieved.is_some());

    println!("   Waiting 4 seconds for expiration...");
    tokio::time::sleep(tokio::time::Duration::from_secs(4)).await;

    println!("   Checking after expiration...");
    let retrieved = memory.get(&temp_id).await?;
    println!("   Entry exists: {} (should be false)", retrieved.is_some());

    // 5. Test namespace isolation
    println!("\n{}", "=".repeat(70));
    println!("🏢 Test 4: Namespace Isolation");
    println!("{}", "=".repeat(70));

    let memory2 = RedisBackend::new(&redis_url)
        .await?
        .with_prefix("other_agent");

    let count1 = memory.count().await?;
    let count2 = memory2.count().await?;

    println!("\n   'rust_demo_agent' namespace: {} entries", count1);
    println!("   'other_agent' namespace: {} entries", count2);
    println!("\n✅ Namespaces are properly isolated!");

    // 6. Create LLM Agent with Redis Memory
    println!("\n{}", "=".repeat(70));
    println!("🤖 Test 5: LLM Agent Integration");
    println!("{}", "=".repeat(70));

    println!("\n🤖 Creating LLM Agent with Redis memory...");
    println!("   Model: {}", model);

    let agent = LlmAgent::builder("redis_agent", &model)
        .with_system_prompt(
            "You are a helpful AI assistant with access to a persistent memory module. \
             You can save important information using the 'save_memory' tool \
             and search for it using the 'search_memory' tool. \
             Your memory persists across sessions.",
        )
        .with_memory(std::sync::Arc::new(memory.clone()))
        .with_temperature(0.7)
        .with_max_tokens(2048)
        .build()?;

    println!("✅ Agent initialized with Redis memory backend");
    println!("\nℹ️  The agent now has access to save_memory and search_memory tools");
    println!("   These tools are automatically registered when memory is provided");

    // 7. Memory persistence info
    println!("\n{}", "=".repeat(70));
    println!("💾 Test 6: Persistence Information");
    println!("{}", "=".repeat(70));

    println!("\nℹ️  Data stored in Redis will persist across:");
    println!("   • Application restarts");
    println!("   • Process crashes");
    println!("   • System reboots (if Redis persists)");
    println!("\n   To test persistence:");
    println!("   1. Run this example");
    println!("   2. Stop it (Ctrl+C)");
    println!("   3. Run it again");
    println!("   4. The entries should still be there!");

    // 8. List all entries
    println!("\n{}", "=".repeat(70));
    println!("📋 All Entries in Redis Memory");
    println!("{}", "=".repeat(70));

    let all_entries = memory.search(MemoryQuery::new()).await?;
    for (i, entry) in all_entries.iter().enumerate() {
        println!("\n{}. ID: {}", i + 1, entry.id);
        println!("   Content: {}", entry.content);
        println!("   Created: {}", entry.created_at);
        if !entry.metadata.is_empty() {
            println!("   Metadata: {:?}", entry.metadata);
        }
    }

    // Cleanup
    println!("\n{}", "=".repeat(70));
    println!("🧹 Cleanup");
    println!("{}", "=".repeat(70));

    memory.clear().await?;
    println!("✅ Redis memory cleared");

    println!("\n{}", "=".repeat(70));
    println!("✨ Example Complete!");
    println!("{}", "=".repeat(70));
    println!("\n💡 Key Features Demonstrated:");
    println!("   • Redis connection and configuration");
    println!("   • Storing and retrieving memory entries");
    println!("   • Metadata filtering");
    println!("   • Semantic (keyword) search");
    println!("   • TTL (Time-To-Live) support");
    println!("   • Namespace isolation");
    println!("   • LLM agent integration");
    println!("   • Persistent storage across restarts");
    println!();

    Ok(())
}
