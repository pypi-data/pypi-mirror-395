//! S3-compatible storage client for bucket operations

use anyhow::{Context, Result};
use aws_sdk_s3::Client;

use crate::config::StorageConfig;

pub struct StorageClient {
    client: Client,
    bucket: String,
    prefix: String,
}

impl StorageClient {
    /// Create a new storage client from config
    pub async fn new(config: &StorageConfig, prefix: &str) -> Result<Self> {
        let mut aws_config = aws_config::defaults(aws_config::BehaviorVersion::latest());

        // Set custom endpoint for Tigris or other S3-compatible services
        if let Some(endpoint) = &config.endpoint {
            aws_config = aws_config.endpoint_url(endpoint);
        }

        // Set region
        if let Some(region) = &config.region {
            aws_config = aws_config.region(aws_config::Region::new(region.clone()));
        }

        let sdk_config = aws_config.load().await;
        let client = Client::new(&sdk_config);

        Ok(Self {
            client,
            bucket: config.bucket.clone(),
            prefix: prefix.to_string(),
        })
    }

    /// Copy all objects from source prefix to fork prefix
    pub async fn copy_to_fork(&self, source_prefix: &str, fork_name: &str) -> Result<String> {
        let fork_prefix = format!("{}{}/", self.prefix, fork_name);

        // List all objects under source prefix
        let mut continuation_token: Option<String> = None;

        loop {
            let mut request = self
                .client
                .list_objects_v2()
                .bucket(&self.bucket)
                .prefix(source_prefix);

            if let Some(token) = &continuation_token {
                request = request.continuation_token(token);
            }

            let response = request
                .send()
                .await
                .context("Failed to list objects in source bucket")?;

            if let Some(contents) = response.contents {
                for object in contents {
                    if let Some(key) = object.key {
                        // Calculate new key by replacing source prefix with fork prefix
                        let relative_path = key.strip_prefix(source_prefix).unwrap_or(&key);
                        let new_key = format!("{}{}", fork_prefix, relative_path);

                        // Copy object
                        let copy_source = format!("{}/{}", self.bucket, key);
                        self.client
                            .copy_object()
                            .bucket(&self.bucket)
                            .key(&new_key)
                            .copy_source(&copy_source)
                            .send()
                            .await
                            .with_context(|| format!("Failed to copy object: {}", key))?;
                    }
                }
            }

            if response.is_truncated == Some(true) {
                continuation_token = response.next_continuation_token;
            } else {
                break;
            }
        }

        Ok(format!("s3://{}/{}", self.bucket, fork_prefix))
    }

    /// Delete all objects under a fork prefix
    pub async fn delete_fork(&self, fork_name: &str) -> Result<()> {
        let fork_prefix = format!("{}{}/", self.prefix, fork_name);

        // List and delete all objects under the fork prefix
        let mut continuation_token: Option<String> = None;

        loop {
            let mut request = self
                .client
                .list_objects_v2()
                .bucket(&self.bucket)
                .prefix(&fork_prefix);

            if let Some(token) = &continuation_token {
                request = request.continuation_token(token);
            }

            let response = request
                .send()
                .await
                .context("Failed to list objects for deletion")?;

            if let Some(contents) = response.contents {
                for object in contents {
                    if let Some(key) = object.key {
                        self.client
                            .delete_object()
                            .bucket(&self.bucket)
                            .key(&key)
                            .send()
                            .await
                            .with_context(|| format!("Failed to delete object: {}", key))?;
                    }
                }
            }

            if response.is_truncated == Some(true) {
                continuation_token = response.next_continuation_token;
            } else {
                break;
            }
        }

        Ok(())
    }

    /// List fork prefixes in storage
    pub async fn list_forks(&self) -> Result<Vec<String>> {
        let response = self
            .client
            .list_objects_v2()
            .bucket(&self.bucket)
            .prefix(&self.prefix)
            .delimiter("/")
            .send()
            .await
            .context("Failed to list fork prefixes")?;

        let mut forks = Vec::new();

        if let Some(prefixes) = response.common_prefixes {
            for prefix in prefixes {
                if let Some(p) = prefix.prefix {
                    // Extract fork name from prefix (e.g., "forks/my-fork/" -> "my-fork")
                    let fork_name = p
                        .strip_prefix(&self.prefix)
                        .unwrap_or(&p)
                        .trim_end_matches('/');
                    if !fork_name.is_empty() {
                        forks.push(fork_name.to_string());
                    }
                }
            }
        }

        Ok(forks)
    }
}
