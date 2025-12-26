use actix_web::{post, web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::process::Command;

#[derive(Deserialize)]
struct GenerateRuleRequest {
    description: String,
}

#[derive(Serialize)]
struct GenerateRuleResponse {
    rule: Option<serde_json::Value>,
    error: Option<String>,
}

#[post("/api/ai/generate-rule")]
pub async fn generate_rule(req: web::Json<GenerateRuleRequest>) -> impl Responder {
    let python_script_path = "..\\ai_modules\\rule_generation_ai.py";
    let description = &req.description;

    let output = Command::new("python")
        .arg(python_script_path)
        .arg(description)
        .output();

    match output {
        Ok(output) => {
            if output.status.success() {
                let stdout = String::from_utf8_lossy(&output.stdout);
                match serde_json::from_str(&stdout) {
                    Ok(rule) => HttpResponse::Ok().json(GenerateRuleResponse { rule: Some(rule), error: None }),
                    Err(e) => HttpResponse::InternalServerError().json(GenerateRuleResponse { rule: None, error: Some(format!("Failed to parse AI response: {}", e)) }),
                }
            } else {
                let stderr = String::from_utf8_lossy(&output.stderr);
                HttpResponse::InternalServerError().json(GenerateRuleResponse { rule: None, error: Some(format!("Python script error: {}", stderr)) }),
            }
        },
        Err(e) => HttpResponse::InternalServerError().json(GenerateRuleResponse { rule: None, error: Some(format!("Failed to execute Python script: {}", e)) }),
    }
}
