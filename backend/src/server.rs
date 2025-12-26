use actix_web::{post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use std::process::Command;

#[derive(Deserialize)]
pub struct GenerateRuleRequest {
    pub description: String,
}

#[derive(Serialize)]
pub struct GenerateRuleResponse {
    pub rule: Option<serde_json::Value>,
    pub error: Option<String>,
}

#[post("/api/ai/generate-rule")]
pub async fn generate_rule_endpoint(req: web::Json<GenerateRuleRequest>) -> impl Responder {
    let python_script_path = "\"..\\ai_modules\\rule_generation_ai.py\"";
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
        Err(e) => {
            if e.kind() == std::io::ErrorKind::NotFound {
                HttpResponse::InternalServerError().json(GenerateRuleResponse { rule: None, error: Some(String::from("Python executable not found. Please ensure Python is installed and in your PATH.")) })
            } else {
                HttpResponse::InternalServerError().json(GenerateRuleResponse { rule: None, error: Some(format!("Failed to execute Python script: {}", e)) })
            }
        },
    }
}

pub async fn run_server() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(generate_rule_endpoint)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
