#!/usr/bin/env python3
"""
ESPHome Dashboard Launcher
Launches the ESPHome dashboard with proper virtual environment activation
Includes first-run configuration UI for easy setup
"""

import os
import sys
import subprocess
import json
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, messagebox

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class ESPHomeConfigUI:
    """Minimalist first-run configuration UI"""

    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.secrets_file = self.config_dir / "secrets.yaml"
        self.config_data = {}

    def show_config_dialog(self):
        """Show configuration dialog and return True if completed"""
        if not TKINTER_AVAILABLE:
            print("⚠️ tkinter not available, skipping GUI setup")
            return self._console_setup()

        root = tk.Tk()
        root.title("ESPHome First Run Setup")
        root.geometry("500x400")
        root.resizable(False, False)

        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (500 // 2)
        y = (root.winfo_screenheight() // 2) - (400 // 2)
        root.geometry(f"500x400+{x}+{y}")

        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame, text="ESPHome Configuration", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # WiFi Settings
        ttk.Label(
            main_frame, text="WiFi Network Name (SSID):", font=("Arial", 10, "bold")
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.wifi_ssid = ttk.Entry(main_frame, width=40)
        self.wifi_ssid.grid(row=1, column=1, pady=5, padx=(10, 0))

        ttk.Label(main_frame, text="WiFi Password:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.wifi_password = ttk.Entry(main_frame, width=40, show="*")
        self.wifi_password.grid(row=2, column=1, pady=5, padx=(10, 0))

        # API Settings
        ttk.Label(
            main_frame, text="API Password (optional):", font=("Arial", 10, "bold")
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.api_password = ttk.Entry(main_frame, width=40)
        self.api_password.grid(row=3, column=1, pady=5, padx=(10, 0))

        # OTA Settings
        ttk.Label(
            main_frame, text="OTA Password (optional):", font=("Arial", 10, "bold")
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.ota_password = ttk.Entry(main_frame, width=40)
        self.ota_password.grid(row=4, column=1, pady=5, padx=(10, 0))

        # Home Assistant (optional)
        ttk.Label(
            main_frame,
            text="Home Assistant URL (optional):",
            font=("Arial", 10, "bold"),
        ).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.ha_url = ttk.Entry(main_frame, width=40)
        self.ha_url.grid(row=5, column=1, pady=5, padx=(10, 0))
        self.ha_url.insert(0, "http://homeassistant.local:8123")

        # Info text
        info_text = tk.Text(
            main_frame,
            height=4,
            width=60,
            wrap=tk.WORD,
            font=("Arial", 9),
            bg="#f0f0f0",
            relief=tk.FLAT,
        )
        info_text.grid(row=6, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        info_text.insert(
            tk.END,
            "This setup creates a secrets.yaml file with your configuration. "
            "Only WiFi SSID is required. You can modify these settings later "
            "by editing config/secrets.yaml or through the ESPHome dashboard.",
        )
        info_text.config(state=tk.DISABLED)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        self.setup_complete = False

        def save_and_continue():
            wifi_ssid = self.wifi_ssid.get().strip()
            if not wifi_ssid:
                messagebox.showerror("Error", "WiFi SSID is required!")
                return

            self.config_data = {
                "wifi_ssid": wifi_ssid,
                "wifi_password": self.wifi_password.get(),
                "api_password": self.api_password.get() or "esphome-api",
                "ota_password": self.ota_password.get() or "esphome-ota",
                "ha_url": self.ha_url.get() or "http://homeassistant.local:8123",
            }

            self.setup_complete = True
            root.destroy()

        def skip_setup():
            self.setup_complete = True
            root.destroy()

        ttk.Button(
            button_frame, text="Save & Continue", command=save_and_continue
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Skip Setup", command=skip_setup).pack(
            side=tk.LEFT, padx=5
        )

        # Set focus to first entry
        self.wifi_ssid.focus()

        # Handle window close
        root.protocol("WM_DELETE_WINDOW", skip_setup)

        root.mainloop()
        return self.setup_complete

    def _console_setup(self):
        """Fallback console setup if tkinter not available"""
        print("\n🔧 ESPHome First Run Setup")
        print("=" * 40)

        wifi_ssid = input("WiFi SSID (required): ").strip()
        if not wifi_ssid:
            print("❌ WiFi SSID is required!")
            return False

        wifi_password = input("WiFi Password: ")
        api_password = (
            input("API Password (press Enter for default): ") or "esphome-api"
        )
        ota_password = (
            input("OTA Password (press Enter for default): ") or "esphome-ota"
        )

        self.config_data = {
            "wifi_ssid": wifi_ssid,
            "wifi_password": wifi_password,
            "api_password": api_password,
            "ota_password": ota_password,
            "ha_url": "http://homeassistant.local:8123",
        }

        return True

    def save_secrets(self):
        """Save configuration to secrets.yaml"""
        if not self.config_data:
            return

        secrets_content = f"""# ESPHome Secrets Configuration
# Generated by first-run setup - edit as needed

# WiFi Configuration
wifi_ssid: "{self.config_data['wifi_ssid']}"
wifi_password: "{self.config_data['wifi_password']}"

# API Configuration
api_password: "{self.config_data['api_password']}"
ota_password: "{self.config_data['ota_password']}"

# Home Assistant Integration
ha_url: "{self.config_data['ha_url']}"
ha_token: "your_long_lived_access_token"

# MQTT Configuration (if using MQTT)
mqtt_broker: "your_mqtt_broker_ip"
mqtt_username: "your_mqtt_username"
mqtt_password: "your_mqtt_password"
"""

        try:
            self.secrets_file.write_text(secrets_content, encoding="utf-8")
            print(f"✅ Configuration saved to {self.secrets_file}")
        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")


def check_first_run(config_dir):
    """Check if this is the first run (no secrets.yaml exists)"""
    secrets_file = Path(config_dir) / "secrets.yaml"
    return not secrets_file.exists()


def main():
    """Launch ESPHome dashboard with optional first-run setup"""
    # Get project root directory
    project_root = Path(__file__).parent.parent
    config_dir = project_root / "config"
    venv_dir = project_root / ".venv"

    # Check if virtual environment exists
    if not venv_dir.exists():
        print("❌ Virtual environment not found at .venv/")
        print("Please run: python -m venv .venv")
        return 1

    # Check if config directory exists
    if not config_dir.exists():
        print("📁 Creating config directory...")
        config_dir.mkdir(exist_ok=True)

    # First-run setup
    if check_first_run(config_dir):
        print("🎉 Welcome to ESPHome! Let's set up your configuration.")

        config_ui = ESPHomeConfigUI(config_dir)
        if config_ui.show_config_dialog():
            config_ui.save_secrets()
            print("✅ Setup complete!")
        else:
            print(
                "⏭️ Setup skipped - you can configure later by editing config/secrets.yaml"
            )

    # Determine the correct python executable
    if os.name == "nt":  # Windows
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:  # Unix-like
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"

    if not python_exe.exists():
        print(f"❌ Python executable not found at {python_exe}")
        return 1

    # Check if ESPHome is installed
    try:
        result = subprocess.run(
            [str(python_exe), "-c", "import esphome"], capture_output=True, text=True
        )
        if result.returncode != 0:
            print("📦 ESPHome not found, installing...")
            subprocess.run([str(pip_exe), "install", "esphome"], check=True)
            print("✅ ESPHome installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install ESPHome")
        return 1

    # Launch ESPHome dashboard
    print(f"🚀 Launching ESPHome dashboard...")
    print(f"📁 Config directory: {config_dir}")
    print(f"🌐 Dashboard will be available at: http://localhost:6052")
    print("Press Ctrl+C to stop the dashboard")

    try:
        subprocess.run(
            [str(python_exe), "-m", "esphome", "dashboard", str(config_dir)],
            cwd=project_root,
            check=True,
        )
    except KeyboardInterrupt:
        print("\n👋 ESPHome dashboard stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start ESPHome dashboard: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
