# ESP32 PlatformIO Project Template

A complete PlatformIO development environment setup for ESP32 projects with professional tooling and automation.

## 🚀 Quick Start

1. **Place your code**: `src/main.cpp` or `src/main.ino`
2. **Build**: `.\build.ps1 build` or `pio run`
3. **Upload**: `.\build.ps1 upload` or `pio run --target upload`
4. **Monitor**: `.\build.ps1 monitor` or `pio device monitor`

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

### PowerShell (Windows)
```powershell
.\build.ps1 build      # Build project
.\build.ps1 upload     # Upload to ESP32
.\build.ps1 monitor    # Serial monitor
.\build.ps1 deploy     # Build + Upload + Monitor
.\build.ps1 clean      # Clean build files
.\build.ps1 devices    # List connected devices
```

### Python Scripts
```bash
python scripts/dev.py build
python scripts/dev.py deploy
python scripts/setup.py    # Setup environment
```

### Direct PlatformIO
```bash
pio run                     # Build
pio run --target upload     # Upload
pio device monitor          # Monitor
pio run --target clean      # Clean
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

## 🔄 Features

- ✅ Multi-environment builds (production/debug/OTA)
- ✅ VS Code integration with IntelliSense
- ✅ Automated build scripts (PowerShell/Python)
- ✅ Serial monitoring and debugging
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Cross-platform development tools

## 📚 Need Help?

- Check `scripts/setup.py` for environment setup
- Use `.\build.ps1 help` for available commands
- Modify `platformio.ini` for project-specific settings