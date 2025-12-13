use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct WorkflowConfig {
    #[serde(default = "default_stop_on_failure")]
    pub stop_on_failure: bool,
    #[serde(default)]
    pub default_retries: u32,
    #[serde(default = "default_pool")]
    pub default_pool: String,
    #[serde(default = "default_secrets_backend")]
    pub secrets_backend: String,
}

impl Default for WorkflowConfig {
    fn default() -> Self {
        Self {
            stop_on_failure: true,
            default_retries: 0,
            default_pool: "CPU".to_string(),
            secrets_backend: "env".to_string(),
        }
    }
}

fn default_stop_on_failure() -> bool { true }
fn default_pool() -> String { "CPU".to_string() }
fn default_secrets_backend() -> String { "env".to_string() }

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct Step {
    pub name: String,
    #[serde(rename = "type")]
    pub step_type: String,
    #[serde(default)]
    pub input: Option<String>,
    #[serde(default)]
    pub inputs: Option<Vec<String>>,
    #[serde(default)]
    pub output: Option<String>,
    #[serde(default)]
    pub outputs: Option<Vec<String>>,
    pub params: HashMap<String, serde_yaml::Value>,
    #[serde(default)]
    pub resource_hint: Option<String>,
    #[serde(default)]
    pub depends_on: Vec<String>,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct WorkflowDefinition {
    pub version: String,
    #[serde(default)]
    pub config: WorkflowConfig,
    pub steps: Vec<Step>,
}
