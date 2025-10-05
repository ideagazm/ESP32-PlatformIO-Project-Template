#!/usr/bin/env python3
"""
Setup script for ESP32 PlatformIO project development environment
"""
import subprocess
import sys
import os
import json


def run_command(cmd, description="", check=True):
    """Run a command and handle errors"""
    if description:
        print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def check_python():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(
            f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported. Need Python 3.7+"
        )
        return False


def check_platformio():
    """Check if PlatformIO is installed"""
    print("\n🔧 Checking PlatformIO installation...")
    if run_command(["pio", "--version"], check=False):
        print("✅ PlatformIO is already installed")
        return True
    else:
        print("❌ PlatformIO not found")
        return False


def install_platformio():
    """Install PlatformIO"""
    print("\n📦 Installing PlatformIO...")
    return run_command([sys.executable, "-m", "pip", "install", "platformio"])


def setup_project():
    """Initialize PlatformIO project"""
    print("\n🏗️ Setting up PlatformIO project...")
    return run_command(["pio", "project", "init", "--ide", "vscode"])


def install_libraries():
    """Install required libraries"""
    print("\n📚 Installing libraries...")
    return run_command(["pio", "lib", "install"])


def check_devices():
    """Check for connected devices"""
    print("\n🔌 Checking for connected devices...")
    return run_command(["pio", "device", "list"])


def create_vscode_settings():
    """Create VS Code settings for PlatformIO"""
    vscode_dir = ".vscode"
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)

    settings_file = os.path.join(vscode_dir, "settings.json")
    settings = {
        "platformio-ide.useBuiltinPIOCore": True,
        "platformio-ide.useDevelopmentPIOCore": False,
        "C_Cpp.intelliSenseEngine": "Tag Parser",
        "files.associations": {"*.ino": "cpp"},
        "platformio-ide.autoRebuildAutocompleteIndex": True,
        "platformio-ide.enableTelemetry": False,
    }

    try:
        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=4)
        print(f"✅ Created VS Code settings: {settings_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create VS Code settings: {e}")
        return False


def main():
    print("🚀 ESP32 PlatformIO Project - Development Environment Setup")
    print("=" * 60)

    steps = [
        ("Check Python version", check_python),
        ("Check PlatformIO", check_platformio),
        ("Install PlatformIO", install_platformio),
        ("Setup project", setup_project),
        ("Install libraries", install_libraries),
        ("Create VS Code settings", create_vscode_settings),
        ("Check devices", check_devices),
    ]

    failed_steps = []

    for step_name, step_func in steps:
        print(f"\n{'='*60}")
        print(f"Step: {step_name}")
        print(f"{'='*60}")

        try:
            if not step_func():
                failed_steps.append(step_name)
                if step_name in ["Check Python version", "Install PlatformIO"]:
                    print(f"❌ Critical step failed: {step_name}")
                    break
        except Exception as e:
            print(f"❌ Error in step '{step_name}': {e}")
            failed_steps.append(step_name)

    print(f"\n{'='*60}")
    print("Setup Summary")
    print(f"{'='*60}")

    if failed_steps:
        print(f"❌ Setup completed with {len(failed_steps)} failed steps:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nPlease resolve the issues above and run setup again.")
    else:
        print("✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Install PlatformIO IDE extension in VS Code")
        print("2. Reload VS Code window")
        print("3. Connect your ESP32 device")
        print("4. Run: python scripts/dev.py build")
        print("5. Run: python scripts/dev.py deploy")


if __name__ == "__main__":
    main()
