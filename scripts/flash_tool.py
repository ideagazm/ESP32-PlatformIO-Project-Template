#!/usr/bin/env python3
"""
ESP32 Flash Management Tool
Backup, restore, and manage ESP32 flash memory
"""
import subprocess
import os
import argparse
from datetime import datetime
import json


class ESP32FlashTool:
    def __init__(self, port="COM3", baudrate=921600):
        self.port = port
        self.baudrate = baudrate
        self.esptool_cmd = ["python", "-m", "esptool", "--port", port, "--baud", str(baudrate)]
    
    def run_esptool(self, args, description=""):
        """Run esptool command"""
        if description:
            print(f"🔧 {description}")
        
        cmd = self.esptool_cmd + args
        print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            if e.stderr:
                print(e.stderr)
            return False
        except FileNotFoundError:
            print("❌ esptool not found. Install with: pip install esptool")
            return False
    
    def chip_info(self):
        """Get chip information"""
        return self.run_esptool(["chip_id"], "Getting chip information")
    
    def flash_info(self):
        """Get flash information"""
        return self.run_esptool(["flash_id"], "Getting flash information")
    
    def backup_flash(self, output_dir="backups"):
        """Create full flash backup"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(output_dir, f"esp32_backup_{timestamp}.bin")
        
        # Read full 4MB flash (adjust size if needed)
        args = ["read_flash", "0x0", "0x400000", backup_file]
        
        if self.run_esptool(args, f"Creating flash backup: {backup_file}"):
            # Create backup info file
            info_file = backup_file.replace(".bin", "_info.json")
            backup_info = {
                "timestamp": timestamp,
                "port": self.port,
                "backup_file": backup_file,
                "flash_size": "4MB",
                "start_address": "0x0",
                "end_address": "0x400000"
            }
            
            try:
                with open(info_file, 'w') as f:
                    json.dump(backup_info, f, indent=2)
                print(f"✅ Backup info saved: {info_file}")
            except Exception as e:
                print(f"⚠️ Could not save backup info: {e}")
            
            return backup_file
        return None
    
    def restore_flash(self, backup_file):
        """Restore flash from backup"""
        if not os.path.exists(backup_file):
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        args = ["write_flash", "0x0", backup_file]
        return self.run_esptool(args, f"Restoring flash from: {backup_file}")
    
    def erase_flash(self):
        """Erase entire flash"""
        print("⚠️ This will erase ALL data on the ESP32!")
        confirm = input("Type 'YES' to confirm: ")
        if confirm != "YES":
            print("❌ Operation cancelled")
            return False
        
        return self.run_esptool(["erase_flash"], "Erasing flash memory")
    
    def backup_partition(self, partition_name, address, size, output_dir="backups"):
        """Backup specific partition"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(output_dir, f"{partition_name}_{timestamp}.bin")
        
        args = ["read_flash", address, size, backup_file]
        
        if self.run_esptool(args, f"Backing up {partition_name} partition"):
            print(f"✅ {partition_name} partition backed up to: {backup_file}")
            return backup_file
        return None
    
    def list_backups(self, backup_dir="backups"):
        """List available backups"""
        if not os.path.exists(backup_dir):
            print(f"❌ Backup directory not found: {backup_dir}")
            return
        
        backups = []
        for file in os.listdir(backup_dir):
            if file.endswith(".bin"):
                file_path = os.path.join(backup_dir, file)
                stat = os.stat(file_path)
                size_mb = stat.st_size / (1024 * 1024)
                modified = datetime.fromtimestamp(stat.st_mtime)
                backups.append((file, size_mb, modified))
        
        if not backups:
            print("📁 No backups found")
            return
        
        print("📁 Available backups:")
        print("-" * 60)
        for filename, size, modified in sorted(backups, key=lambda x: x[2], reverse=True):
            print(f"{filename:<30} {size:>8.2f} MB  {modified.strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    parser = argparse.ArgumentParser(description="ESP32 Flash Management Tool")
    parser.add_argument("-p", "--port", default="COM3", help="Serial port")
    parser.add_argument("-b", "--baudrate", type=int, default=921600, help="Baud rate")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Info commands
    subparsers.add_parser("chip-info", help="Get chip information")
    subparsers.add_parser("flash-info", help="Get flash information")
    
    # Backup commands
    backup_parser = subparsers.add_parser("backup", help="Create full flash backup")
    backup_parser.add_argument("-o", "--output", default="backups", help="Output directory")
    
    restore_parser = subparsers.add_parser("restore", help="Restore flash from backup")
    restore_parser.add_argument("backup_file", help="Backup file to restore")
    
    # Partition backup
    partition_parser = subparsers.add_parser("backup-partition", help="Backup specific partition")
    partition_parser.add_argument("name", help="Partition name")
    partition_parser.add_argument("address", help="Start address (e.g., 0x10000)")
    partition_parser.add_argument("size", help="Size (e.g., 0x100000)")
    partition_parser.add_argument("-o", "--output", default="backups", help="Output directory")
    
    # Other commands
    subparsers.add_parser("erase", help="Erase entire flash")
    list_parser = subparsers.add_parser("list", help="List available backups")
    list_parser.add_argument("-d", "--directory", default="backups", help="Backup directory")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tool = ESP32FlashTool(args.port, args.baudrate)
    
    if args.command == "chip-info":
        tool.chip_info()
    elif args.command == "flash-info":
        tool.flash_info()
    elif args.command == "backup":
        backup_file = tool.backup_flash(args.output)
        if backup_file:
            print(f"\n✅ Flash backup completed: {backup_file}")
    elif args.command == "restore":
        if tool.restore_flash(args.backup_file):
            print(f"\n✅ Flash restore completed")
    elif args.command == "backup-partition":
        backup_file = tool.backup_partition(args.name, args.address, args.size, args.output)
        if backup_file:
            print(f"\n✅ Partition backup completed: {backup_file}")
    elif args.command == "erase":
        if tool.erase_flash():
            print(f"\n✅ Flash erase completed")
    elif args.command == "list":
        tool.list_backups(args.directory)


if __name__ == "__main__":
    main()