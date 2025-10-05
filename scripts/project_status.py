#!/usr/bin/env python3
"""
ESP32 Project Status and Health Check
"""
import os
import subprocess
import json
from datetime import datetime
import glob


def check_file_exists(file_path, description):
    """Check if a file exists and return status"""
    exists = os.path.exists(file_path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists


def get_file_size(file_path):
    """Get file size in human readable format"""
    if not os.path.exists(file_path):
        return "N/A"
    
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def run_command(cmd, capture_output=True):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, capture_output=capture_output, text=True, check=True)
        return True, result.stdout if capture_output else ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, ""


def check_platformio():
    """Check PlatformIO installation and project status"""
    print("\n🔧 PlatformIO Status")
    print("-" * 30)
    
    # Check PlatformIO installation
    pio_installed, version = run_command(["pio", "--version"])
    if pio_installed:
        print(f"✅ PlatformIO installed: {version.strip()}")
    else:
        print("❌ PlatformIO not found")
        return False
    
    # Check project initialization
    if os.path.exists(".pio"):
        print("✅ Project initialized")
    else:
        print("❌ Project not initialized")
        return False
    
    # Check build status
    build_success, _ = run_command(["pio", "run", "--dry-run"])
    if build_success:
        print("✅ Project configuration valid")
    else:
        print("❌ Project configuration issues")
    
    return True


def check_project_structure():
    """Check project file structure"""
    print("\n📁 Project Structure")
    print("-" * 30)
    
    required_files = [
        ("platformio.ini", "PlatformIO configuration"),
        ("src/main.example.cpp", "Main source file"),
        ("build.ps1", "Build script"),
        ("scripts/setup.py", "Setup script"),
        ("scripts/dev.py", "Development script")
    ]
    
    optional_files = [
        ("include/", "Include directory"),
        ("lib/", "Library directory"),
        ("data/", "Data directory"),
        (".vscode/", "VS Code settings"),
        ("README.md", "Documentation")
    ]
    
    all_good = True
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    print("\nOptional files:")
    for file_path, description in optional_files:
        check_file_exists(file_path, description)
    
    return all_good


def check_build_artifacts():
    """Check build artifacts and sizes"""
    print("\n🔨 Build Artifacts")
    print("-" * 30)
    
    build_dir = ".pio/build/esp32dev"
    if not os.path.exists(build_dir):
        print("❌ No build artifacts found. Run 'pio run' first.")
        return False
    
    artifacts = [
        ("firmware.elf", "Main firmware"),
        ("firmware.bin", "Flash binary"),
        ("bootloader.bin", "Bootloader"),
        ("partitions.bin", "Partition table")
    ]
    
    for artifact, description in artifacts:
        artifact_path = os.path.join(build_dir, artifact)
        if os.path.exists(artifact_path):
            size = get_file_size(artifact_path)
            print(f"✅ {description}: {size}")
        else:
            print(f"❌ {description}: Not found")
    
    return True


def check_devices():
    """Check connected devices"""
    print("\n🔌 Connected Devices")
    print("-" * 30)
    
    devices_found, output = run_command(["pio", "device", "list"])
    if devices_found and output.strip():
        lines = output.strip().split('\n')
        device_count = len([line for line in lines if line.startswith('COM') or line.startswith('/dev/')])
        print(f"✅ Found {device_count} device(s)")
        
        # Show device details
        for line in lines:
            if line.startswith('COM') or line.startswith('/dev/'):
                print(f"   📱 {line}")
    else:
        print("❌ No devices found")
        return False
    
    return True


def check_logs():
    """Check log files"""
    print("\n📋 Log Files")
    print("-" * 30)
    
    log_dir = "logs"
    if not os.path.exists(log_dir):
        print("📁 No logs directory")
        return True
    
    log_files = glob.glob(os.path.join(log_dir, "*"))
    if not log_files:
        print("📁 No log files found")
        return True
    
    for log_file in sorted(log_files)[-5:]:  # Show last 5 files
        size = get_file_size(log_file)
        modified = datetime.fromtimestamp(os.path.getmtime(log_file))
        print(f"📄 {os.path.basename(log_file)}: {size} ({modified.strftime('%Y-%m-%d %H:%M')})")
    
    return True


def check_libraries():
    """Check installed libraries"""
    print("\n📚 Libraries")
    print("-" * 30)
    
    lib_success, output = run_command(["pio", "lib", "list"])
    if lib_success:
        if "No items" in output:
            print("📦 No external libraries installed")
        else:
            lines = output.strip().split('\n')
            lib_count = len([line for line in lines if line.strip() and not line.startswith('Library')])
            print(f"✅ {lib_count} libraries installed")
    else:
        print("❌ Could not check libraries")
    
    return True


def generate_status_report():
    """Generate comprehensive status report"""
    print("🚀 ESP32 Project Status Report")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checks = [
        ("Project Structure", check_project_structure),
        ("PlatformIO", check_platformio),
        ("Build Artifacts", check_build_artifacts),
        ("Connected Devices", check_devices),
        ("Libraries", check_libraries),
        ("Log Files", check_logs)
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n❌ Error in {check_name}: {e}")
            results[check_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Summary")
    print(f"{'='*50}")
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Project is healthy and ready for development!")
    else:
        print("⚠️ Some issues found. Please review the failed checks above.")
    
    return passed == total


def main():
    healthy = generate_status_report()
    exit(0 if healthy else 1)


if __name__ == "__main__":
    main()