#!/usr/bin/env python3
"""
Benign test script - legitimate implementations for false positive testing
"""

import os
import json
import hashlib
import subprocess
from pathlib import Path

# Legitimate API call - weather data fetch
def get_weather(city: str) -> dict:
    """
    Fetch weather data from public API.
    Documented in SKILL.md as a core feature.
    """
    import requests
    
    # Safe API call to public weather service
    response = requests.get(
        f"https://api.weather.com/v1/current?city={city}",
        timeout=10
    )
    response.raise_for_status()
    return response.json()

# Legitimate file operation - creating output
def save_results(data: dict, output_path: str):
    """
    Save processing results to user-specified location.
    Only writes to allowed directories.
    """
    # Validate path is within allowed directory
    allowed_dir = Path.home() / "Documents" / "SkillOutput"
    target = Path(output_path).resolve()
    
    if not str(target).startswith(str(allowed_dir)):
        raise ValueError("Output path not in allowed directory")
    
    # Safe file write
    with open(target, 'w') as f:
        json.dump(data, f, indent=2)

# Legitimate environment access - reading config
def get_config():
    """
    Read configuration from environment variables.
    Only reads specific, non-sensitive variables.
    """
    config = {
        'debug_mode': os.environ.get('SKILL_DEBUG', 'false').lower() == 'true',
        'output_format': os.environ.get('SKILL_FORMAT', 'json'),
        'max_retries': int(os.environ.get('SKILL_RETRIES', '3')),
    }
    return config

# Legitimate hash operation - data verification
def verify_file_integrity(file_path: str, expected_hash: str) -> bool:
    """
    Verify file integrity using SHA-256 hash.
    Used for validating downloaded resources.
    """
    sha256 = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    
    return sha256.hexdigest() == expected_hash

# Legitimate subprocess - running external tool
def convert_image(input_path: str, output_path: str):
    """
    Convert image format using ImageMagick.
    Uses safe argument passing (no shell=True).
    """
    # Safe: argument list, no shell, validated paths
    cmd = [
        'convert',
        str(Path(input_path).resolve()),
        str(Path(output_path).resolve())
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
        # No shell=True - safe
    )
    
    return result.returncode == 0

# Legitimate temp file cleanup
def cleanup_temp_files():
    """
    Clean up temporary files created by this skill.
    Only removes files from skill's temp directory.
    """
    temp_dir = Path(os.environ.get('TEMP', '/tmp')) / 'skill-test-benign'
    
    if temp_dir.exists():
        for file in temp_dir.glob('*.tmp'):
            file.unlink()  # Safe: only in skill temp dir

if __name__ == "__main__":
    # Demo legitimate operations
    config = get_config()
    print(f"Config: {config}")
    
    # Cleanup
    cleanup_temp_files()
    print("Cleanup complete")
