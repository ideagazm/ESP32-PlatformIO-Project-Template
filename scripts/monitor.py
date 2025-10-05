#!/usr/bin/env python3
"""
Enhanced Serial Monitor for ESP32 with logging and filtering
"""
import serial
import time
import argparse
import os
from datetime import datetime
import re
import threading
import queue


class ESPMonitor:
    def __init__(self, port, baudrate=115200, log_file=None, filter_pattern=None):
        self.port = port
        self.baudrate = baudrate
        self.log_file = log_file
        self.filter_pattern = re.compile(filter_pattern) if filter_pattern else None
        self.running = False
        self.serial_conn = None
        self.log_queue = queue.Queue()
        
    def connect(self):
        """Connect to serial port"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"✅ Connected to {self.port} at {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            print(f"❌ Failed to connect to {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from serial port"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 Disconnected from serial port")
    
    def log_writer(self):
        """Background thread for writing logs"""
        if not self.log_file:
            return
            
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                while self.running:
                    try:
                        log_entry = self.log_queue.get(timeout=1)
                        f.write(log_entry)
                        f.flush()
                    except queue.Empty:
                        continue
        except Exception as e:
            print(f"❌ Log writing error: {e}")
    
    def format_line(self, line, timestamp=True):
        """Format a line with timestamp and filtering"""
        if timestamp:
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            formatted = f"[{ts}] {line}"
        else:
            formatted = line
            
        return formatted
    
    def should_display(self, line):
        """Check if line should be displayed based on filter"""
        if not self.filter_pattern:
            return True
        return bool(self.filter_pattern.search(line))
    
    def monitor(self, show_timestamps=True, auto_scroll=True):
        """Start monitoring serial output"""
        if not self.connect():
            return False
            
        self.running = True
        
        # Start log writer thread
        log_thread = None
        if self.log_file:
            log_thread = threading.Thread(target=self.log_writer, daemon=True)
            log_thread.start()
            print(f"📝 Logging to: {self.log_file}")
        
        print("🔍 Monitoring serial output (Ctrl+C to stop)")
        print("-" * 60)
        
        try:
            buffer = ""
            while self.running:
                if self.serial_conn.in_waiting > 0:
                    try:
                        data = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='replace')
                        buffer += data
                        
                        # Process complete lines
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.rstrip('\r')
                            
                            if line and self.should_display(line):
                                formatted_line = self.format_line(line, show_timestamps)
                                print(formatted_line)
                                
                                # Queue for logging
                                if self.log_file:
                                    self.log_queue.put(formatted_line + '\n')
                    
                    except UnicodeDecodeError:
                        # Handle binary data
                        print("[BINARY DATA]")
                        
                time.sleep(0.01)  # Small delay to prevent high CPU usage
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")
        finally:
            self.running = False
            self.disconnect()
            
            if log_thread:
                log_thread.join(timeout=2)
        
        return True
    
    def send_command(self, command):
        """Send a command to the device"""
        if not self.serial_conn or not self.serial_conn.is_open:
            print("❌ Not connected to device")
            return False
            
        try:
            self.serial_conn.write((command + '\n').encode('utf-8'))
            print(f"📤 Sent: {command}")
            return True
        except Exception as e:
            print(f"❌ Failed to send command: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Enhanced ESP32 Serial Monitor")
    parser.add_argument("-p", "--port", default="COM3", help="Serial port (default: COM3)")
    parser.add_argument("-b", "--baudrate", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("-l", "--log", help="Log file path")
    parser.add_argument("-f", "--filter", help="Regex filter pattern")
    parser.add_argument("--no-timestamps", action="store_true", help="Disable timestamps")
    parser.add_argument("-c", "--command", help="Send a single command and exit")
    
    args = parser.parse_args()
    
    # Create logs directory if logging
    if args.log:
        log_dir = os.path.dirname(args.log)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    monitor = ESPMonitor(
        port=args.port,
        baudrate=args.baudrate,
        log_file=args.log,
        filter_pattern=args.filter
    )
    
    if args.command:
        # Send single command mode
        if monitor.connect():
            monitor.send_command(args.command)
            time.sleep(1)  # Wait for response
            monitor.disconnect()
    else:
        # Interactive monitoring mode
        monitor.monitor(show_timestamps=not args.no_timestamps)


if __name__ == "__main__":
    main()