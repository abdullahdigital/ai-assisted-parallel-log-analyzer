import datetime
import random
import os

def generate_log_entry(timestamp, log_id):
    levels = ["INFO", "WARN", "ERROR", "DEBUG"]
    messages = [
        "User logged in successfully.",
        "Failed login attempt.",
        "Resource accessed.",
        "Database query executed.",
        "API call received.",
        "System health check.",
        "Unauthorized access detected.",
        "File download initiated.",
        "Configuration updated.",
        "Service restarted."
    ]
    ip_addresses = [f"192.168.1.{i}" for i in range(1, 255)] + [f"10.0.0.{i}" for i in range(1, 255)]
    user_ids = [f"user_{i:04d}" for i in range(1, 100)]

    level = random.choice(levels)
    message = random.choice(messages)
    ip_address = random.choice(ip_addresses)
    user_id = random.choice(user_ids) if random.random() > 0.2 else "N/A" # Some logs might not have a user ID

    return f"{timestamp.isoformat()}Z {level} {ip_address} {user_id} {message} (LogID:{log_id})"

def generate_log_file(file_path, num_entries):
    print(f"Generating {num_entries} log entries to {file_path}...")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        start_time = datetime.datetime.now() - datetime.timedelta(days=30) # Logs from the last 30 days
        for i in range(num_entries):
            # Distribute logs over time, with some bursts
            time_offset_seconds = random.uniform(0, 30 * 24 * 60 * 60)
            if random.random() < 0.1: # 10% chance of a burst (logs within a few seconds)
                time_offset_seconds -= random.uniform(0, 60)
            
            timestamp = start_time + datetime.timedelta(seconds=time_offset_seconds)
            f.write(generate_log_entry(timestamp, i + 1) + "\n")
            if (i + 1) % 50000 == 0:
                print(f"Generated {i + 1}/{num_entries} entries...")
    print(f"Finished generating {num_entries} log entries.")

if __name__ == "__main__":
    output_dir = "frontend/public/data"
    output_file = os.path.join(output_dir, "example_log.txt")
    
    # Generate between 500,000 and 1,000,000 entries
    num_entries = random.randint(500000, 1000000) 
    
    generate_log_file(output_file, num_entries)
