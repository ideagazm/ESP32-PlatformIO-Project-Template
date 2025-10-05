# ESP32 PlatformIO Project Template

A complete PlatformIO development environment setup for ESP32 projects with professional tooling, automation, and advanced development features.

## 🚀 Quick Start

1. **Setup Environment**: `.\build.ps1 setup`
2. **Check Status**: `.\build.ps1 status`
3. **Place your code**: `src/main.cpp` or `src/main.ino`
4. **Build**: `.\build.ps1 build`
5. **Upload**: `.\build.ps1 upload`
6. **Monitor**: `.\build.ps1 monitor`

## 📁 Project Structure

```
├── src/                    # Your source code (.cpp, .ino, .h files)
├── lib/                    # Custom libraries (optional)
├── data/                   # SPIFFS/LittleFS data files
├── scripts/                # Development automation scripts
├── .vscode/                # VS Code integration
├── platformio.ini          # PlatformIO configuration
└── build.ps1              # Windows build script
```

### File Placement
- **Main file**: `src/main.cpp` (recommended) or `src/main.ino`
- **Headers/Source**: All `.cpp`, `.c`, `.h`, `.hpp` files in `src/`
- **Custom libraries**: Create subdirectories in `lib/`
- **Data files**: SPIFFS files in `data/`

## 🛠️ Development Commands

### Core Development
```powershell
.\build.ps1 build      # Build project
.\build.ps1 upload     # Upload to ESP32
.\build.ps1 monitor    # Serial monitor
.\build.ps1 deploy     # Build + Upload + Monitor
.\build.ps1 clean      # Clean build files
.\build.ps1 devices    # List connected devices
.\build.ps1 size       # Analyze build size and memory usage
```

### Advanced Tools
```powershell
.\build.ps1 wifi           # Generate WiFi configuration
.\build.ps1 monitor-enhanced # Enhanced serial monitor with logging
.\build.ps1 backup         # Create flash memory backup
.\build.ps1 flash-info     # Get chip and flash information
.\build.ps1 logs           # Show recent log files
.\build.ps1 status         # Check project health and status
```

### Debug & OTA
```powershell
.\build.ps1 debug      # Build debug version
.\build.ps1 ota        # Upload via OTA (Over-The-Air)
.\build.ps1 uploadfs   # Upload SPIFFS filesystem
```

### Setup & Maintenance
```powershell
.\build.ps1 setup      # Run development environment setup
.\build.ps1 install    # Install dependencies
.\build.ps1 update     # Update libraries
.\build.ps1 check      # Run code analysis
```

### Python Scripts
```bash
python scripts/dev.py build
python scripts/dev.py deploy
python scripts/setup.py              # Setup environment
python scripts/wifi_config.py        # WiFi configuration generator
python scripts/monitor.py            # Enhanced serial monitor
python scripts/flash_tool.py         # Flash management
python scripts/ota_update.py         # OTA update manager
python scripts/project_status.py     # Project health check
```

## 🔧 Build Environments

- **esp32dev** (default): Production build, optimized
- **esp32dev_debug**: Debug build with verbose logging  
- **esp32dev_ota**: Over-the-air update capable

Build specific environment: `pio run -e esp32dev_debug`

## 📋 Hardware Setup

1. Connect ESP32 development board via USB
2. Install ESP32 drivers if needed
3. Check connection: `.\build.ps1 devices`
4. Update `upload_port` in `platformio.ini` if needed

## 🔄 Advanced Features

### Core Development
- ✅ Multi-environment builds (production/debug/OTA)
- ✅ VS Code integration with IntelliSense
- ✅ Automated build scripts (PowerShell/Python)
- ✅ Cross-platform development tools
- ✅ Code analysis and size optimization

### WiFi & Networking
- 🌐 **WiFi Configuration Generator**: Secure credential management
- 📡 **Access Point Fallback**: Automatic AP mode configuration
- 🔐 **Security**: Auto-generated secure passwords
- 🌍 **OTA Updates**: Over-the-air firmware deployment

### Monitoring & Debugging
- 📊 **Enhanced Serial Monitor**: Real-time logging with filtering
- 📝 **Automatic Logging**: Timestamped logs with rotation
- 🔍 **Regex Filtering**: Filter serial output by patterns
- 📈 **Memory Analysis**: Build size and usage tracking

### Flash Management
- 💾 **Flash Backup/Restore**: Complete device backup capability
- 🔧 **Partition Management**: Individual partition backup
- 📱 **Device Information**: Chip ID, flash size, SDK version
- 🛡️ **Data Protection**: MD5 verification for integrity

### Project Management
- 📊 **Health Monitoring**: Comprehensive project status checks
- 🔍 **Dependency Tracking**: Library and tool verification
- 📋 **Build Artifact Analysis**: Size and memory usage reports
- 🚨 **Issue Detection**: Automatic problem identification

### Development Workflow
- 🚀 **One-Command Deploy**: Build, upload, and monitor in one step
- 🔄 **Hot Reload**: Fast development iteration
- 📦 **Library Management**: Automated dependency handling
- 🎯 **Multi-Target Support**: Debug, production, and OTA builds

## 📚 Need Help?

- Check `scripts/setup.py` for environment setup
- Use `.\build.ps1 help` for available commands
- Modify `platformio.ini` for project-specific settings
##
 🛠️ Tool Details

### WiFi Configuration (`.\build.ps1 wifi`)
Generates secure WiFi credentials and configuration files:
- Creates `data/wifi_config.json` for runtime configuration
- Generates `include/wifi_config.h` for compile-time constants
- Supports both station and access point modes
- Auto-generates secure passwords

### Enhanced Monitor (`.\build.ps1 monitor-enhanced`)
Advanced serial monitoring with:
- Real-time logging to `logs/serial.log`
- Regex pattern filtering
- Timestamp formatting
- Background logging thread

### Flash Management (`.\build.ps1 backup`)
Complete flash memory management:
- Full device backup with metadata
- Individual partition backup
- Restore from backup files
- Flash information and chip details

### OTA Updates
Over-the-air firmware deployment:
```bash
python scripts/ota_update.py 192.168.1.100 -f .pio/build/esp32dev/firmware.bin
```

### Project Status (`.\build.ps1 status`)
Comprehensive health check covering:
- Project structure validation
- PlatformIO installation status
- Build artifact analysis
- Connected device detection
- Library dependency status

## 📁 Generated Files

The tools create several directories and files:
```
├── logs/                   # Serial monitor logs, OTA update logs
├── backups/               # Flash memory backups with metadata
├── data/                  # WiFi configuration JSON
├── include/               # Generated header files
└── .pio/                  # PlatformIO build artifacts
```

## 🔧 Configuration

### WiFi Setup
1. Run `.\build.ps1 wifi` to generate configuration
2. Include `#include "wifi_config.h"` in your code
3. Use the defined constants: `WIFI_SSID`, `WIFI_PASSWORD`, etc.

### OTA Setup
1. Build with OTA environment: `.\build.ps1 ota`
2. Configure device IP in `platformio.ini`
3. Use OTA update script for remote deployment

### Monitoring Setup
1. Enhanced monitor: `.\build.ps1 monitor-enhanced`
2. Filter output: `python scripts/monitor.py -f "ERROR|WARNING"`
3. Custom log file: `python scripts/monitor.py -l custom.log`

## 🚨 Troubleshooting

### Common Issues
- **Device not found**: Check USB connection and drivers
- **Build fails**: Run `.\build.ps1 status` for diagnostics
- **OTA fails**: Verify device IP and network connectivity
- **Monitor issues**: Check COM port in `platformio.ini`

### Getting Help
- Run `.\build.ps1 status` for comprehensive diagnostics
- Check `logs/` directory for error details
- Use `.\build.ps1 help` for command reference
- Verify setup with `.\build.ps1 setup`