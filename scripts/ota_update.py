#!/usr/bin/env python3
"""
OTA (Over-The-Air) Update Manager for ESP32
"""
import requests
import hashlib
import os
import argparse
import json
from datetime import datetime


class OTAManager:
    def __init__(self, device_ip, auth_password="admin", port=3232):
        self.device_ip = device_ip
        self.auth_password = auth_password
        self.port = port
        self.base_url = f"http://{device_ip}:{port}"
    
    def check_device_status(self):
        """Check if device is reachable and OTA ready"""
        try:
            response = requests.get(f"{self.base_url}/status", timeout=5)
            if response.status_code == 200:
                print(f"✅ Device {self.device_ip} is online and OTA ready")
                return True
            else:
                print(f"❌ Device returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot reach device {self.device_ip}: {e}")
            return False
    
    def get_device_info(self):
        """Get device information"""
        try:
            response = requests.get(f"{self.base_url}/info", timeout=5)
            if response.status_code == 200:
                info = response.json()
                print("📱 Device Information:")
                print(f"   Chip ID: {info.get('chip_id', 'Unknown')}")
                print(f"   Free Heap: {info.get('free_heap', 'Unknown')} bytes")
                print(f"   Sketch Size: {info.get('sketch_size', 'Unknown')} bytes")
                print(f"   Flash Size: {info.get('flash_size', 'Unknown')} bytes")
                print(f"   SDK Version: {info.get('sdk_version', 'Unknown')}")
                return info
            else:
                print(f"❌ Could not get device info: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting device info: {e}")
            return None
    
    def calculate_md5(self, file_path):
        """Calculate MD5 hash of firmware file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"❌ Error calculating MD5: {e}")
            return None
    
    def upload_firmware(self, firmware_path):
        """Upload firmware via OTA"""
        if not os.path.exists(firmware_path):
            print(f"❌ Firmware file not found: {firmware_path}")
            return False
        
        file_size = os.path.getsize(firmware_path)
        md5_hash = self.calculate_md5(firmware_path)
        
        print(f"📦 Uploading firmware: {firmware_path}")
        print(f"   Size: {file_size} bytes")
        print(f"   MD5: {md5_hash}")
        
        try:
            with open(firmware_path, 'rb') as f:
                files = {'firmware': f}
                data = {
                    'MD5': md5_hash,
                    'auth': self.auth_password
                }
                
                print("🚀 Starting OTA update...")
                response = requests.post(
                    f"{self.base_url}/update",
                    files=files,
                    data=data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    print("✅ OTA update successful!")
                    print("🔄 Device is rebooting...")
                    return True
                else:
                    print(f"❌ OTA update failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ OTA update error: {e}")
            return False
    
    def reboot_device(self):
        """Reboot the device"""
        try:
            data = {'auth': self.auth_password}
            response = requests.post(f"{self.base_url}/reboot", data=data, timeout=10)
            if response.status_code == 200:
                print("🔄 Device reboot initiated")
                return True
            else:
                print(f"❌ Reboot failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Reboot error: {e}")
            return False
    
    def create_update_log(self, firmware_path, success):
        """Create update log entry"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, "ota_updates.json")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "device_ip": self.device_ip,
            "firmware_path": firmware_path,
            "firmware_size": os.path.getsize(firmware_path) if os.path.exists(firmware_path) else 0,
            "md5_hash": self.calculate_md5(firmware_path) if os.path.exists(firmware_path) else None,
            "success": success
        }
        
        # Load existing logs
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Add new entry
        logs.append(log_entry)
        
        # Keep only last 50 entries
        logs = logs[-50:]
        
        # Save logs
        try:
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            print(f"📝 Update log saved to: {log_file}")
        except Exception as e:
            print(f"⚠️ Could not save update log: {e}")


def main():
    parser = argparse.ArgumentParser(description="ESP32 OTA Update Manager")
    parser.add_argument("device_ip", help="Device IP address or hostname")
    parser.add_argument("-f", "--firmware", help="Firmware file path")
    parser.add_argument("-p", "--password", default="admin", help="OTA password")
    parser.add_argument("--port", type=int, default=3232, help="OTA port")
    parser.add_argument("--check", action="store_true", help="Only check device status")
    parser.add_argument("--info", action="store_true", help="Get device information")
    parser.add_argument("--reboot", action="store_true", help="Reboot device")
    
    args = parser.parse_args()
    
    ota = OTAManager(args.device_ip, args.password, args.port)
    
    if args.check:
        ota.check_device_status()
        return
    
    if args.info:
        ota.get_device_info()
        return
    
    if args.reboot:
        ota.reboot_device()
        return
    
    if not args.firmware:
        print("❌ Firmware file required for OTA update")
        parser.print_help()
        return
    
    # Full OTA update process
    print("🚀 ESP32 OTA Update Manager")
    print("=" * 40)
    
    if not ota.check_device_status():
        return
    
    ota.get_device_info()
    
    success = ota.upload_firmware(args.firmware)
    ota.create_update_log(args.firmware, success)
    
    if success:
        print("\n✅ OTA update completed successfully!")
    else:
        print("\n❌ OTA update failed!")


if __name__ == "__main__":
    main()