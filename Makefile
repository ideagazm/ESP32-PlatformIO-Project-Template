# ESP32 Relay Controller - Makefile
# Requires PlatformIO to be installed

.PHONY: help build upload monitor clean devices setup deploy debug ota

# Default target
help:
	@echo "ESP32 Relay Controller - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  build      - Build the project"
	@echo "  upload     - Upload firmware to device"
	@echo "  monitor    - Start serial monitor"
	@echo "  clean      - Clean build files"
	@echo "  deploy     - Full deployment (clean, build, upload, monitor)"
	@echo ""
	@echo "Advanced:"
	@echo "  debug      - Build debug version"
	@echo "  ota        - Upload via OTA (Over-The-Air)"
	@echo "  uploadfs   - Upload SPIFFS filesystem"
	@echo "  devices    - List connected devices"
	@echo ""
	@echo "Setup:"
	@echo "  setup      - Run development environment setup"
	@echo "  install    - Install dependencies"

# Basic commands
build:
	pio run

upload:
	pio run --target upload

monitor:
	pio device monitor

clean:
	pio run --target clean

# Utility commands
devices:
	pio device list

uploadfs:
	pio run --target uploadfs

# Advanced builds
debug:
	pio run -e esp32dev_debug

ota:
	pio run -e esp32dev_ota --target upload

# Compound commands
deploy: clean build upload monitor

# Setup commands
setup:
	python scripts/setup.py

install:
	pip install -r requirements.txt

# Quick development cycle
dev: build upload

# Build all environments
build-all:
	pio run -e esp32dev
	pio run -e esp32dev_debug

# Check project
check:
	pio check

# Update libraries
update:
	pio lib update

# Show project info
info:
	pio project data