use std::fs;
use std::path::Path;
use serde_json;

use crate::models::ParsingRule;

pub fn load_parsing_rules<P: AsRef<Path>>(path: P) -> Result<Vec<ParsingRule>, String> {
    let file_content = fs::read_to_string(path)
        .map_err(|e| format!("Failed to read parsing rules file: {}", e))?;

    let rules: Vec<ParsingRule> = serde_json::from_str(&file_content)
        .map_err(|e| format!("Failed to deserialize parsing rules: {}", e))?;

    Ok(rules)
}
