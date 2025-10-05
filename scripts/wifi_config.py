#!/usr/bin/env python3
"""
WiFi Configuration Generator for ESP32 Projects
Generates secure WiFi credentials and configuration files
"""
import json
import os
import secrets
import string
from getpass import getpass


def generate_random_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_wifi_config():
    """Create WiFi configuration"""
    print("🌐 WiFi Configuration Generator")
    print("=" * 40)
    
    # Get WiFi credentials
    ssid = input("WiFi SSID: ").strip()
    if not ssid:
        print("❌ SSID cannot be empty")
        return False
    
    password = getpass("WiFi Password (leave empty to generate): ").strip()
    if not password:
        password = generate_random_password()
        print(f"🔐 Generated password: {password}")
    
    # Optional AP mode settings
    print("\n📡 Access Point Settings (for fallback mode)")
    ap_ssid = input(f"AP SSID (default: ESP32-{secrets.token_hex(3).upper()}): ").strip()
    if not ap_ssid:
        ap_ssid = f"ESP32-{secrets.token_hex(3).upper()}"
    
    ap_password = input("AP Password (leave empty to generate): ").strip()
    if not ap_password:
        ap_password = generate_random_password(12)
        print(f"🔐 Generated AP password: {ap_password}")
    
    # Create configuration
    config = {
        "wifi": {
            "ssid": ssid,
            "password": password,
            "timeout_ms": 10000,
            "retry_attempts": 3
        },
        "ap": {
            "ssid": ap_ssid,
            "password": ap_password,
            "channel": 1,
            "max_connections": 4,
            "hidden": False
        },
        "network": {
            "hostname": "esp32-device",
            "enable_mdns": True,
            "static_ip": {
                "enabled": False,
                "ip": "192.168.1.100",
                "gateway": "192.168.1.1",
                "subnet": "255.255.255.0",
                "dns1": "8.8.8.8",
                "dns2": "8.8.4.4"
            }
        }
    }
    
    # Save to data directory
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    config_file = os.path.join(data_dir, "wifi_config.json")
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n✅ WiFi configuration saved to: {config_file}")
        
        # Generate C++ header file
        header_content = f'''#ifndef WIFI_CONFIG_H
#define WIFI_CONFIG_H

// WiFi Configuration
#define WIFI_SSID "{ssid}"
#define WIFI_PASSWORD "{password}"
#define WIFI_TIMEOUT_MS {config["wifi"]["timeout_ms"]}
#define WIFI_RETRY_ATTEMPTS {config["wifi"]["retry_attempts"]}

// Access Point Configuration
#define AP_SSID "{ap_ssid}"
#define AP_PASSWORD "{ap_password}"
#define AP_CHANNEL {config["ap"]["channel"]}
#define AP_MAX_CONNECTIONS {config["ap"]["max_connections"]}

// Network Configuration
#define HOSTNAME "{config["network"]["hostname"]}"
#define ENABLE_MDNS {str(config["network"]["enable_mdns"]).lower()}

// Static IP Configuration (set STATIC_IP_ENABLED to true to use)
#define STATIC_IP_ENABLED {str(config["network"]["static_ip"]["enabled"]).lower()}
#define STATIC_IP "{config["network"]["static_ip"]["ip"]}"
#define GATEWAY_IP "{config["network"]["static_ip"]["gateway"]}"
#define SUBNET_MASK "{config["network"]["static_ip"]["subnet"]}"
#define DNS1_IP "{config["network"]["static_ip"]["dns1"]}"
#define DNS2_IP "{config["network"]["static_ip"]["dns2"]}"

#endif // WIFI_CONFIG_H
'''
        
        include_dir = "include"
        if not os.path.exists(include_dir):
            os.makedirs(include_dir)
        
        header_file = os.path.join(include_dir, "wifi_config.h")
        with open(header_file, 'w') as f:
            f.write(header_content)
        print(f"✅ C++ header saved to: {header_file}")
        
        print(f"\n📋 Configuration Summary:")
        print(f"   WiFi SSID: {ssid}")
        print(f"   AP SSID: {ap_ssid}")
        print(f"   Hostname: {config['network']['hostname']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False


def main():
    if not create_wifi_config():
        exit(1)
    
    print(f"\n💡 Next steps:")
    print(f"1. Include 'wifi_config.h' in your main.cpp")
    print(f"2. Use the defined constants for WiFi connection")
    print(f"3. Upload filesystem: pio run --target uploadfs")
    print(f"4. Build and upload your project")


if __name__ == "__main__":
    main()