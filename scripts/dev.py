#!/usr/bin/env python3
"""
Development helper script for ESP32 PlatformIO projects
"""
import subprocess
import sys
import argparse
import time

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    if description:
        print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False

def build_project(env="esp32dev"):
    """Build the project"""
    return run_command(["pio", "run", "-e", env], f"Building project ({env})")

def upload_project(env="esp32dev"):
    """Upload the project"""
    return run_command(["pio", "run", "-e", env, "--target", "upload"], f"Uploading to device ({env})")

def monitor_device():
    """Monitor serial output"""
    return run_command(["pio", "device", "monitor"], "Starting serial monitor")

def clean_project():
    """Clean build files"""
    return run_command(["pio", "run", "--target", "clean"], "Cleaning build files")

def upload_filesystem():
    """Upload SPIFFS filesystem"""
    return run_command(["pio", "run", "--target", "uploadfs"], "Uploading SPIFFS filesystem")

def check_devices():
    """List available devices"""
    return run_command(["pio", "device", "list"], "Checking available devices")

def full_deploy(env="esp32dev"):
    """Full deployment: clean, build, upload, monitor"""
    steps = [
        ("Clean", lambda: clean_project()),
        ("Build", lambda: build_project(env)),
        ("Upload", lambda: upload_project(env)),
        ("Monitor", lambda: monitor_device())
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        print(f"Step: {step_name}")
        print(f"{'='*50}")
        
        if not step_func():
            print(f"❌ Failed at step: {step_name}")
            return False
            
        if step_name != "Monitor":  # Don't wait after monitor starts
            time.sleep(1)
    
    return True

def main():
    parser = argparse.ArgumentParser(description="ESP32 PlatformIO Project Development Helper")
    parser.add_argument("action", choices=[
        "build", "upload", "monitor", "clean", "uploadfs", 
        "devices", "deploy", "debug-build", "ota-upload"
    ], help="Action to perform")
    parser.add_argument("-e", "--env", default="esp32dev", 
                       choices=["esp32dev", "esp32dev_debug", "esp32dev_ota"],
                       help="Environment to use")
    
    args = parser.parse_args()
    
    print("🚀 ESP32 PlatformIO Project - Development Helper")
    print(f"Environment: {args.env}")
    
    success = False
    
    if args.action == "build":
        success = build_project(args.env)
    elif args.action == "upload":
        success = upload_project(args.env)
    elif args.action == "monitor":
        success = monitor_device()
    elif args.action == "clean":
        success = clean_project()
    elif args.action == "uploadfs":
        success = upload_filesystem()
    elif args.action == "devices":
        success = check_devices()
    elif args.action == "deploy":
        success = full_deploy(args.env)
    elif args.action == "debug-build":
        success = build_project("esp32dev_debug")
    elif args.action == "ota-upload":
        success = upload_project("esp32dev_ota")
    
    if success:
        print(f"\n✅ {args.action.title()} completed successfully!")
    else:
        print(f"\n❌ {args.action.title()} failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()