import json

def generate_explanation(metrics: list[dict]) -> str:
    """
    Generates a natural language explanation and recommendations based on the provided metrics.
    """
    if not metrics:
        return "No metrics provided for explanation."

    latest_metrics = metrics[-1]
    explanation_parts = []

    explanation_parts.append(f"The latest log analysis run in '{latest_metrics.get('mode', 'N/A')}' mode processed "
                             f"{latest_metrics.get('total_logs_processed', 0):,} logs in "
                             f"{latest_metrics.get('execution_time_ms', 0):.2f} milliseconds, achieving a rate of "
                             f"{latest_metrics.get('logs_per_second', 0):.2f} logs per second.")

    alerts = latest_metrics.get('alerts_generated', [])
    if alerts:
        explanation_parts.append(f"During this run, {len(alerts)} alerts were generated. "
                                 "These indicate potential security incidents or anomalies.")
        for i, alert in enumerate(alerts[:3]): # Limit to first 3 alerts for brevity
            explanation_parts.append(f"- Alert {i+1}: A '{alert.get('alert_type', 'N/A')}' alert was triggered "
                                     f"due to '{alert.get('description', 'N/A')}' at {alert.get('timestamp', 'N/A')}.")
        if len(alerts) > 3:
            explanation_parts.append(f"  (and {len(alerts) - 3} more alerts...)")
    else:
        explanation_parts.append("No alerts were generated in this analysis run, indicating a clean scan or that current rules did not detect any threats.")

    recommendations = []
    if latest_metrics.get('logs_per_second', 0) < 1000:
        recommendations.append("Consider optimizing log parsing and analysis logic for better performance, especially in sequential mode.")
    if len(alerts) > 5:
        recommendations.append("Review the generated alerts immediately to understand the nature of potential threats and take corrective actions.")
    if latest_metrics.get('mode') == 'sequential' and latest_metrics.get('total_logs_processed', 0) > 10000:
        recommendations.append("For large log volumes, consider utilizing parallel or distributed analysis modes to significantly reduce processing time.")

    if recommendations:
        explanation_parts.append("\nRecommendations:")
        for i, rec in enumerate(recommendations):
            explanation_parts.append(f"{i+1}. {rec}")

    return "\n".join(explanation_parts)

if __name__ == '__main__':
    # Example Usage:
    sample_metrics = [
        {
            "total_logs_processed": 150000,
            "execution_time_ms": 1200.50,
            "logs_per_second": 124950.00,
            "alerts_generated": [
                {
                    "id": "alert-1",
                    "timestamp": "2024-01-01T10:00:00Z",
                    "alert_type": "BruteForce",
                    "description": "Multiple failed login attempts from 192.168.1.10",
                    "log_entry_sample": {"ip_address": "192.168.1.10", "user": "admin"}
                },
                {
                    "id": "alert-2",
                    "timestamp": "2024-01-01T10:01:00Z",
                    "alert_type": "HighFrequencyRequest",
                    "description": "Unusual number of requests to /api/v1/sensitive_data from 10.0.0.5",
                    "log_entry_sample": {"ip_address": "10.0.0.5", "path": "/api/v1/sensitive_data"}
                }
            ],
            "mode": "parallel"
        },
        {
            "total_logs_processed": 500000,
            "execution_time_ms": 3500.75,
            "logs_per_second": 142847.00,
            "alerts_generated": [
                {
                    "id": "alert-3",
                    "timestamp": "2024-01-01T11:00:00Z",
                    "alert_type": "SuspiciousIp",
                    "description": "Connection from known malicious IP 172.16.0.1",
                    "log_entry_sample": {"ip_address": "172.16.0.1"}
                },
                {
                    "id": "alert-4",
                    "timestamp": "2024-01-01T11:05:00Z",
                    "alert_type": "BruteForce",
                    "description": "15 failed login attempts from 192.168.1.11",
                    "log_entry_sample": {"ip_address": "192.168.1.11", "user": "guest"}
                },
                {
                    "id": "alert-5",
                    "timestamp": "2024-01-01T11:10:00Z",
                    "alert_type": "HighFrequencyRequest",
                    "description": "2000 requests in 1 minute to /login from 10.0.0.6",
                    "log_entry_sample": {"ip_address": "10.0.0.6", "path": "/login"}
                },
                {
                    "id": "alert-6",
                    "timestamp": "2024-01-01T11:15:00Z",
                    "alert_type": "Custom",
                    "description": "Unusual data exfiltration pattern detected",
                    "log_entry_sample": {"source": "internal", "destination": "external"}
                }
            ],
            "mode": "distributed"
        }
    ]

    explanation = generate_explanation(sample_metrics)
    print(explanation)
