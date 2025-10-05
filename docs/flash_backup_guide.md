# ESP32 Flash Backup Guide

## Overview
The flash backup tool allows you to create complete backups of your ESP32's flash memory, including firmware, bootloader, and data partitions.

## Prerequisites
- ESP32 connected via USB
- PlatformIO and esptool installed
- ESP32 in download mode for backup operations

## Putting ESP32 in Download Mode

### Method 1: Hardware Buttons
1. Hold down the **BOOT** button (GPIO0)
2. Press and release the **RESET** button (EN)
3. Release the **BOOT** button
4. ESP32 is now in download mode

### Method 2: Automatic (if supported)
Some ESP32 boards support automatic download mode via DTR/RTS signals.

## Backup Commands

### Full Flash Backup
```powershell
.\build.ps1 backup
```
Creates a complete 4MB flash backup in `backups/` directory.

### Individual Commands
```bash
# Get chip information
python scripts/flash_tool.py chip-info

# Get flash information  
python scripts/flash_tool.py flash-info

# Create backup
python scripts/flash_tool.py backup

# List backups
python scripts/flash_tool.py list

# Restore from backup
python scripts/flash_tool.py restore backup_file.bin
```

### Partition Backup
```bash
# Backup specific partition
python scripts/flash_tool.py backup-partition app0 0x10000 0x100000
```

## Common Partition Addresses
- **Bootloader**: 0x1000 (4KB)
- **Partition Table**: 0x8000 (4KB) 
- **NVS**: 0x9000 (20KB)
- **App0**: 0x10000 (1MB)
- **App1**: 0x110000 (1MB) - for OTA
- **SPIFFS**: 0x210000 (1.5MB)

## Backup Files
Backups are stored in `backups/` with:
- **Timestamp**: `esp32_backup_YYYYMMDD_HHMMSS.bin`
- **Metadata**: `esp32_backup_YYYYMMDD_HHMMSS_info.json`

## Troubleshooting

### "Wrong boot mode detected"
- ESP32 is not in download mode
- Follow download mode steps above
- Check USB connection

### "Failed to connect"
- Verify COM port in `platformio.ini`
- Check USB drivers
- Try different USB cable/port

### "Permission denied"
- Close serial monitor
- Close other applications using the port
- Run as administrator if needed

## Safety Notes
⚠️ **Important**: 
- Always backup before flashing new firmware
- Verify backup integrity before major changes
- Keep multiple backup copies for critical projects
- Test restore process on development boards first

## Recovery
If your ESP32 becomes unresponsive:
1. Put device in download mode
2. Restore from backup: `python scripts/flash_tool.py restore backup_file.bin`
3. Or erase and reflash: `python scripts/flash_tool.py erase`