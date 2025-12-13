//! Configuration file parsing for .forkstack.toml

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};


/// Main configuration structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub database: DatabaseConfig,
    #[serde(default)]
    pub storage: HashMap<String, StorageConfig>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DatabaseConfig {
    pub provider: String,
    pub organization: String,
    pub production: String,
    pub group: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageConfig {
    pub provider: String,
    pub bucket: String,
    pub endpoint: Option<String>,
    pub region: Option<String>,
    pub prefix: Option<String>,
}

impl Config {
    /// Load config from .forkstack.toml in current directory or parents
    pub fn load() -> Result<Self> {
        let config_path = Self::find_config_file()?;
        Self::load_from_path(&config_path)
    }

    /// Load config from a specific path
    pub fn load_from_path(path: &Path) -> Result<Self> {
        let content = std::fs::read_to_string(path)
            .with_context(|| format!("Failed to read config file: {}", path.display()))?;

        let config: Config = toml::from_str(&content)
            .with_context(|| format!("Failed to parse config file: {}", path.display()))?;

        Ok(config)
    }

    /// Find .forkstack.toml by walking up from current directory
    fn find_config_file() -> Result<PathBuf> {
        let mut current = std::env::current_dir()?;

        loop {
            let config_path = current.join(".forkstack.toml");
            if config_path.exists() {
                return Ok(config_path);
            }

            // Also check forkstack.toml (without dot)
            let alt_path = current.join("forkstack.toml");
            if alt_path.exists() {
                return Ok(alt_path);
            }

            if !current.pop() {
                anyhow::bail!(
                    "No .forkstack.toml found. Create one with:\n\n\
                    [database]\n\
                    provider = \"turso\"\n\
                    organization = \"your-org\"\n\
                    production = \"your-db-name\"\n"
                );
            }
        }
    }

    /// Get the database group (defaults to "default")
    pub fn database_group(&self) -> String {
        self.database.group.clone().unwrap_or_else(|| "default".to_string())
    }

    /// Get storage configs as a vec
    pub fn storage_configs(&self) -> Vec<(&String, &StorageConfig)> {
        self.storage.iter().collect()
    }
}

impl StorageConfig {
    /// Get the prefix for forks (defaults to "forks/")
    pub fn fork_prefix(&self) -> String {
        self.prefix.clone().unwrap_or_else(|| "forks/".to_string())
    }
}

/// Example config for documentation
pub fn example_config() -> &'static str {
    r#"[database]
provider = "turso"
organization = "my-org"
production = "my-app-prod"
group = "default"  # optional

[storage.uploads]
provider = "tigris"
bucket = "my-uploads-bucket"
endpoint = "https://fly.storage.tigris.dev"
prefix = "forks/"

[storage.assets]
provider = "s3"
bucket = "my-assets-bucket"
region = "us-east-1"
prefix = "forks/"
"#
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    #[test]
    fn test_parse_minimal_config() {
        let config_str = r#"
[database]
provider = "turso"
organization = "my-org"
production = "my-db"
"#;
        let config: Config = toml::from_str(config_str).unwrap();

        assert_eq!(config.database.provider, "turso");
        assert_eq!(config.database.organization, "my-org");
        assert_eq!(config.database.production, "my-db");
        assert_eq!(config.database.group, None);
        assert!(config.storage.is_empty());
    }

    #[test]
    fn test_parse_full_config() {
        let config_str = r#"
[database]
provider = "turso"
organization = "my-org"
production = "my-db"
group = "default"

[storage.uploads]
provider = "tigris"
bucket = "my-uploads"
endpoint = "https://fly.storage.tigris.dev"
prefix = "forks/"

[storage.assets]
provider = "s3"
bucket = "my-assets"
region = "us-east-1"
"#;
        let config: Config = toml::from_str(config_str).unwrap();

        assert_eq!(config.database.group, Some("default".to_string()));
        assert_eq!(config.storage.len(), 2);

        let uploads = config.storage.get("uploads").unwrap();
        assert_eq!(uploads.provider, "tigris");
        assert_eq!(uploads.bucket, "my-uploads");
        assert_eq!(
            uploads.endpoint,
            Some("https://fly.storage.tigris.dev".to_string())
        );

        let assets = config.storage.get("assets").unwrap();
        assert_eq!(assets.provider, "s3");
        assert_eq!(assets.bucket, "my-assets");
        assert_eq!(assets.region, Some("us-east-1".to_string()));
    }

    #[test]
    fn test_database_group_default() {
        let config_str = r#"
[database]
provider = "turso"
organization = "my-org"
production = "my-db"
"#;
        let config: Config = toml::from_str(config_str).unwrap();
        assert_eq!(config.database_group(), "default");
    }

    #[test]
    fn test_storage_fork_prefix_default() {
        let config_str = r#"
[database]
provider = "turso"
organization = "my-org"
production = "my-db"

[storage.uploads]
provider = "tigris"
bucket = "my-bucket"
"#;
        let config: Config = toml::from_str(config_str).unwrap();
        let uploads = config.storage.get("uploads").unwrap();
        assert_eq!(uploads.fork_prefix(), "forks/");
    }

    #[test]
    fn test_storage_fork_prefix_custom() {
        let config_str = r#"
[database]
provider = "turso"
organization = "my-org"
production = "my-db"

[storage.uploads]
provider = "tigris"
bucket = "my-bucket"
prefix = "dev-forks/"
"#;
        let config: Config = toml::from_str(config_str).unwrap();
        let uploads = config.storage.get("uploads").unwrap();
        assert_eq!(uploads.fork_prefix(), "dev-forks/");
    }

    #[test]
    fn test_load_from_path() {
        let mut file = NamedTempFile::new().unwrap();
        writeln!(
            file,
            r#"
[database]
provider = "turso"
organization = "test-org"
production = "test-db"
"#
        )
        .unwrap();

        let config = Config::load_from_path(file.path()).unwrap();
        assert_eq!(config.database.organization, "test-org");
    }
}
