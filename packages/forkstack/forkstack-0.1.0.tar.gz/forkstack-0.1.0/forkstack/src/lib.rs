//! forkstack - instant, isolated development environments
//!
//! Create zero-copy forks of your database and storage for instant,
//! isolated development environments.

pub mod config;
pub mod storage;
pub mod turso;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

use config::Config;
use storage::StorageClient;
use turso::TursoClient;

/// A fork represents an isolated development environment
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Fork {
    pub name: String,
    pub database_url: String,
    pub storage_url: String,
    pub created_at: u64,
}

impl Fork {
    /// Returns a human-readable "time ago" string
    pub fn created_ago(&self) -> String {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        let diff = now.saturating_sub(self.created_at);

        if diff < 60 {
            "just now".to_string()
        } else if diff < 3600 {
            format!("{} mins ago", diff / 60)
        } else if diff < 86400 {
            format!("{} hours ago", diff / 3600)
        } else {
            format!("{} days ago", diff / 86400)
        }
    }
}

/// Create a new fork
pub async fn create_fork(name: Option<String>) -> Result<Fork> {
    let config = Config::load()?;
    let fork_name = name.unwrap_or_else(generate_fork_name);
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();

    // Create Turso database fork
    let turso = TursoClient::new(&config.database.organization)?;
    let db_info = turso
        .create_fork(&fork_name, &config.database.production, &config.database_group())
        .await?;

    let database_url = format!("libsql://{}", db_info.hostname);

    // Copy storage for each configured bucket
    let mut storage_urls = Vec::new();
    for (bucket_name, storage_config) in config.storage_configs() {
        let storage = StorageClient::new(storage_config, &storage_config.fork_prefix()).await?;
        let url = storage.copy_to_fork("", &fork_name).await?;
        storage_urls.push(format!("{}: {}", bucket_name, url));
    }

    let fork = Fork {
        name: fork_name,
        database_url,
        storage_url: storage_urls.join("\n"),
        created_at: now,
    };

    Ok(fork)
}

/// List all forks
pub async fn list_forks() -> Result<Vec<Fork>> {
    let config = Config::load()?;

    // Get databases from Turso that look like forks
    let turso = TursoClient::new(&config.database.organization)?;
    let databases = turso.list_databases().await?;

    // Filter to databases that aren't the production one
    let forks: Vec<Fork> = databases
        .into_iter()
        .filter(|db| db.name != config.database.production)
        .map(|db| Fork {
            name: db.name.clone(),
            database_url: format!("libsql://{}", db.hostname),
            storage_url: String::new(), // Could query S3 but adds latency
            created_at: 0,              // Turso API doesn't return this easily
        })
        .collect();

    Ok(forks)
}

/// Delete a fork
pub async fn delete_fork(name: &str) -> Result<()> {
    let config = Config::load()?;

    // Delete Turso database
    let turso = TursoClient::new(&config.database.organization)?;
    turso.delete_database(name).await?;

    // Delete storage for each configured bucket
    for (_bucket_name, storage_config) in config.storage_configs() {
        let storage = StorageClient::new(storage_config, &storage_config.fork_prefix()).await?;
        storage.delete_fork(name).await?;
    }

    Ok(())
}

/// Generate a random fork name
fn generate_fork_name() -> String {
    let adjectives = ["swift", "bright", "calm", "bold", "keen"];
    let nouns = ["fork", "branch", "leaf", "wave", "spark"];

    use std::collections::hash_map::RandomState;
    use std::hash::{BuildHasher, Hasher};

    let mut hasher = RandomState::new().build_hasher();
    hasher.write_u64(
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64,
    );
    let hash = hasher.finish();

    let adj = adjectives[(hash % adjectives.len() as u64) as usize];
    let noun = nouns[((hash >> 8) % nouns.len() as u64) as usize];
    let num = (hash >> 16) % 1000;

    format!("{}-{}-{}", adj, noun, num)
}
