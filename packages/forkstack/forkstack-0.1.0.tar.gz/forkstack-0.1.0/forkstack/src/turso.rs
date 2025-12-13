//! Turso API client for database operations

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};

const TURSO_API_BASE: &str = "https://api.turso.tech/v1";

pub struct TursoClient {
    client: reqwest::Client,
    token: String,
    organization: String,
}

#[derive(Debug, Serialize)]
struct CreateDatabaseRequest {
    name: String,
    group: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    seed: Option<SeedConfig>,
}

#[derive(Debug, Serialize)]
struct SeedConfig {
    #[serde(rename = "type")]
    seed_type: String,
    name: String,
}

#[derive(Debug, Deserialize)]
struct CreateDatabaseResponse {
    database: DatabaseInfo,
}

#[derive(Debug, Deserialize)]
pub struct DatabaseInfo {
    #[serde(rename = "DbId")]
    pub db_id: String,
    #[serde(rename = "Name")]
    pub name: String,
    #[serde(rename = "Hostname")]
    pub hostname: String,
}

#[derive(Debug, Deserialize)]
struct ListDatabasesResponse {
    databases: Vec<DatabaseListItem>,
}

#[derive(Debug, Deserialize)]
pub struct DatabaseListItem {
    #[serde(rename = "Name")]
    pub name: String,
    #[serde(rename = "Hostname")]
    pub hostname: String,
}

impl TursoClient {
    /// Create a new Turso client
    pub fn new(organization: &str) -> Result<Self> {
        let token = std::env::var("TURSO_API_TOKEN")
            .or_else(|_| std::env::var("TURSO_AUTH_TOKEN"))
            .context("TURSO_API_TOKEN or TURSO_AUTH_TOKEN environment variable not set")?;

        Ok(Self {
            client: reqwest::Client::new(),
            token,
            organization: organization.to_string(),
        })
    }

    /// Create a database forked from another database
    pub async fn create_fork(&self, name: &str, from_db: &str, group: &str) -> Result<DatabaseInfo> {
        let url = format!(
            "{}/organizations/{}/databases",
            TURSO_API_BASE, self.organization
        );

        let request = CreateDatabaseRequest {
            name: name.to_string(),
            group: group.to_string(),
            seed: Some(SeedConfig {
                seed_type: "database".to_string(),
                name: from_db.to_string(),
            }),
        };

        let response = self
            .client
            .post(&url)
            .header("Authorization", format!("Bearer {}", self.token))
            .json(&request)
            .send()
            .await
            .context("Failed to send request to Turso API")?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            anyhow::bail!("Turso API error ({}): {}", status, body);
        }

        let result: CreateDatabaseResponse = response
            .json()
            .await
            .context("Failed to parse Turso API response")?;

        Ok(result.database)
    }

    /// List all databases in the organization
    pub async fn list_databases(&self) -> Result<Vec<DatabaseListItem>> {
        let url = format!(
            "{}/organizations/{}/databases",
            TURSO_API_BASE, self.organization
        );

        let response = self
            .client
            .get(&url)
            .header("Authorization", format!("Bearer {}", self.token))
            .send()
            .await
            .context("Failed to send request to Turso API")?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            anyhow::bail!("Turso API error ({}): {}", status, body);
        }

        let result: ListDatabasesResponse = response
            .json()
            .await
            .context("Failed to parse Turso API response")?;

        Ok(result.databases)
    }

    /// Delete a database
    pub async fn delete_database(&self, name: &str) -> Result<()> {
        let url = format!(
            "{}/organizations/{}/databases/{}",
            TURSO_API_BASE, self.organization, name
        );

        let response = self
            .client
            .delete(&url)
            .header("Authorization", format!("Bearer {}", self.token))
            .send()
            .await
            .context("Failed to send request to Turso API")?;

        if !response.status().is_success() {
            let status = response.status();
            let body = response.text().await.unwrap_or_default();
            anyhow::bail!("Turso API error ({}): {}", status, body);
        }

        Ok(())
    }
}
