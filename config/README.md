# ESPHome Configuration

This directory contains ESPHome device configuration files (.yaml).

## Setup

1. **First Run Setup**:
   ```bash
   # Launch ESPHome with automatic setup
   python scripts/esphome_dashboard.py
   # OR
   .\build.ps1 esphome
   ```
   
   On first run, a configuration dialog will appear to set up:
   - WiFi credentials
   - API passwords
   - OTA passwords
   - Home Assistant URL (optional)

2. **Manual Setup** (alternative):
   ```bash
   # Activate virtual environment
   .venv\Scripts\activate

   # Install ESPHome
   pip install esphome
   
   # Launch dashboard
   esphome dashboard config/
   ```

3. **Access Dashboard**:
   Open your browser and navigate to `http://localhost:6052`

## Features Available

- **Compile**: Build firmware for your devices
- **Flash**: Upload firmware to ESP devices
- **Logs**: View real-time device logs
- **OTA**: Over-the-air updates for deployed devices
- **Configuration**: Web-based YAML editor

## Directory Structure

```
config/
├── README.md           # This file
├── device1.yaml        # Example device configuration
└── secrets.yaml        # Sensitive configuration (WiFi passwords, etc.)
```

## Getting Started

1. Create a new device configuration file (e.g., `my_device.yaml`)
2. Use the ESPHome dashboard to edit and manage your configurations
3. Flash your first device using the dashboard interface

## Security & Git Protection

### Protected Files
The following files are automatically excluded from git commits:
- `secrets.yaml` - Main secrets file
- `*secrets*` - Any file with "secrets" in the name
- `*.secrets.*` - Files with secrets extension
- `private*` - Private configuration files
- `*_credentials.*`, `*_auth.*`, `*_keys.*` - Credential files

### Safe to Commit
- `example_*` - Example configurations
- `template_*` - Template files
- Device configurations **without** sensitive data
- `README.md` and documentation

### Best Practices
1. **Use secrets.yaml**: Store all sensitive data in the secrets file
2. **Reference secrets**: Use `!secret key_name` in device configs
3. **Check before commit**: Always review files before committing
4. **Template approach**: Create `device_template.yaml` for sharing configs

### Example Safe Device Config
```yaml
esphome:
  name: my-device

wifi:
  ssid: !secret wifi_ssid          # Safe - references secrets
  password: !secret wifi_password  # Safe - references secrets

api:
  password: !secret api_password   # Safe - references secrets
```