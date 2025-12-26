import json

def generate_rule_from_natural_language(description: str) -> dict:
    """
    Generates a structured rule (JSON) from a natural language description.
    This is a placeholder for an actual AI model integration.
    """
    # In a real application, this would involve a call to an NLP model (e.g., OpenAI, Gemini, etc.)
    # that can parse the natural language and extract rule parameters.
    # For demonstration purposes, we'll use a simple heuristic or a mock response.

    rule = {
        "name": "Generated Rule",
        "description": description,
        "rule_type": "Custom",
        "threshold": 1,
        "time_window_seconds": 60,
    }

    description_lower = description.lower()

    if "failed logins" in description_lower or "brute force" in description_lower:
        rule["name"] = "BruteForceAttempt"
        rule["rule_type"] = "BruteForce"
        rule["threshold"] = 5 # Default threshold for brute force
        if "more than" in description_lower:
            try:
                parts = description_lower.split("more than")
                threshold_str = parts[1].strip().split(" ")[0]
                rule["threshold"] = int(threshold_str)
            except (ValueError, IndexError):
                pass # Keep default
        if "in" in description_lower and "minutes" in description_lower:
            try:
                parts = description_lower.split("in")
                time_str = parts[1].strip().split(" ")[0]
                rule["time_window_seconds"] = int(time_str) * 60
            except (ValueError, IndexError):
                pass # Keep default

    elif "high frequency request" in description_lower or "unusual number of requests" in description_lower:
        rule["name"] = "HighFrequencyRequest"
        rule["rule_type"] = "HighFrequencyRequest"
        rule["threshold"] = 100 # Default threshold for high frequency
        if "more than" in description_lower:
            try:
                parts = description_lower.split("more than")
                threshold_str = parts[1].strip().split(" ")[0]
                rule["threshold"] = int(threshold_str)
            except (ValueError, IndexError):
                pass # Keep default
        if "in" in description_lower and ("seconds" in description_lower or "minutes" in description_lower):
            try:
                parts = description_lower.split("in")
                time_str = parts[1].strip().split(" ")[0]
                if "minutes" in description_lower:
                    rule["time_window_seconds"] = int(time_str) * 60
                else:
                    rule["time_window_seconds"] = int(time_str)
            except (ValueError, IndexError):
                pass # Keep default

    elif "suspicious ip" in description_lower or "malicious ip" in description_lower:
        rule["name"] = "SuspiciousIpAccess"
        rule["rule_type"] = "SuspiciousIp"
        rule["threshold"] = 1 # Even one access from suspicious IP is an alert
        rule["time_window_seconds"] = 3600 # Monitor for an hour

    return rule

if __name__ == '__main__':
    # Example Usage:
    print("Generating rule for: Detect more than 10 failed logins from the same IP in 5 minutes")
    rule1 = generate_rule_from_natural_language("Detect more than 10 failed logins from the same IP in 5 minutes")
    print(json.dumps(rule1, indent=2))

    print("\nGenerating rule for: Alert if there are an unusual number of requests (over 500) to /admin in 30 seconds")
    rule2 = generate_rule_from_natural_language("Alert if there are an unusual number of requests (over 500) to /admin in 30 seconds")
    print(json.dumps(rule2, indent=2))

    print("\nGenerating rule for: Flag any connection from a known malicious IP address")
    rule3 = generate_rule_from_natural_language("Flag any connection from a known malicious IP address")
    print(json.dumps(rule3, indent=2))

    print("\nGenerating rule for: Custom rule for unusual activity")
    rule4 = generate_rule_from_natural_language("Custom rule for unusual activity")
    print(json.dumps(rule4, indent=2))
