use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct LogEntry {
    pub timestamp: DateTime<Utc>,
    pub ip_address: String,
    pub user_id: Option<String>,
    pub event_type: String,
    pub details: HashMap<String, String>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum AlertType {
    BruteForce,
    HighFrequencyRequest,
    SuspiciousIpBehavior,
    Custom(String),
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Alert {
    pub id: String,
    pub timestamp: DateTime<Utc>,
    pub alert_type: AlertType,
    pub description: String,
    pub log_entry_sample: Option<LogEntry>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Metrics {
    pub total_logs_processed: usize,
    pub alerts_generated: Vec<Alert>,
    pub mode: String, // Sequential, Parallel, Distributed
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Rule {
    pub name: String,
    pub description: String,
    pub rule_type: RuleType,
    pub threshold: usize,
    pub time_window_seconds: u64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum RuleType {
    BruteForce,
    HighFrequencyRequest,
    SuspiciousIp,
    Custom(String),
}

#[derive(Debug, Serialize, Deserialize)]
pub enum WorkerMessage {
    LogChunk(Vec<LogEntry>),
    Rules(Vec<Rule>),
    StartAnalysis,
    Shutdown,
}

#[derive(Debug, Serialize, Deserialize)]
pub enum MasterMessage {
    AnalysisResult(Metrics),
    Error(String),
    Ack,
}
