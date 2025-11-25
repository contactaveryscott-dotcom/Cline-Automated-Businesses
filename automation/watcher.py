import os
import time
import json
import subprocess

INCOMING_DIR = "automation/incoming"
RENDERED_DIR = "automation/rendered"
LOGS_DIR = "automation/logs"

def validate_json_schema(data):
    required = ["title", "script", "storyboard", "duration"]
    return all(field in data for field in required)

def log_event(message):
    with open(os.path.join(LOGS_DIR, "watcher.log"), "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")

def process_script(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        if not validate_json_schema(data):
            log_event(f"Invalid schema: {file_path}")
            return
        log_event(f"Valid script detected: {file_path}")
        output_path = os.path.join(RENDERED_DIR, os.path.splitext(os.path.basename(file_path))[0] + ".mp4")
        subprocess.run(["python3", "automation/renderer_ffmpeg.py", file_path, output_path], check=True)
        log_event(f"Rendered: {output_path}")
    except Exception as e:
        log_event(f"Error processing {file_path}: {e}")

def watch():
    processed = set()
    log_event("Watcher started.")
    while True:
        files = [f for f in os.listdir(INCOMING_DIR) if f.endswith(".json")]
        for fname in files:
            fpath = os.path.join(INCOMING_DIR, fname)
            if fpath not in processed:
                process_script(fpath)
                processed.add(fpath)
        time.sleep(5)

if __name__ == "__main__":
    watch()
