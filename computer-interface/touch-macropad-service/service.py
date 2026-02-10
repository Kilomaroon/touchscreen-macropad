# /usr/local/bin/touch-macropad-service.py
from enum import Enum
import re
import serial
import time
import logging
import signal
import sys
import traceback
from pathlib import Path
from sound_handler import SoundHandler
from evdev_handler import EvdevHandler, ecodes
from cfg import actions, sound_dir
from enums import Action, SoundAction

class SerialService:
    def __init__(self, config_file='/etc/touch-macropad-service.conf'):
        self.config_file = config_file
        self.running = False
        self.serial = None
        self.packetMatch = re.compile("^(\\d+)[\\+\\-]$")
        self.logger = self.setup_logging()

        self.evdev_handler = EvdevHandler(self.logger)
        self.sound_handler = SoundHandler(self.logger, base_dir=sound_dir)
        
    def setup_logging(self):
        """Setup logging for systemd"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def load_config(self):
        """Load configuration"""
        config = {
            'port': '/dev/touchscreenmacropad',
            'baudrate': 19200,
            'timeout': 1,
            'retry_interval': 5
        }
        
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            if key in config:
                                if key == 'baudrate' or key == 'timeout' or key == 'retry_interval':
                                    config[key] = int(value)
                                else:
                                    config[key] = value
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            
        return config
        
    def connect_serial(self, config):
        """Connect to serial device with retry"""
        while self.running:
            try:
                self.logger.info(f"Attempting to connect to {config['port']}")
                self.serial = serial.Serial(
                    port=config['port'],
                    baudrate=config['baudrate'],
                    timeout=config['timeout']
                )
                self.logger.info(f"Connected to {config['port']}")
                return True
                
            except Exception as e:
                self.logger.error(f"Connection failed: {e}")
                time.sleep(config['retry_interval'])
                
        return False
        
    def process_data(self, data):
        """Process received data"""
        
        packet = None
        try:
            # try to read packet
            data_string = data.decode('utf-8', errors='ignore').strip()
            packet = self.packetMatch.match(data_string)
            self.logger.info(f"Received: {data_string}")
            if packet == None:
                self.logger.error(f"Invalid data received from device: {data_string}")

            # handle action
            if data_string not in actions.keys() or not actions[data_string]:
                pass
            elif actions[data_string][0] == Action.KEYS:
                self.evdev_handler.handle(actions[data_string][1])
            elif actions[data_string][0] == Action.SOUND:
                self.sound_handler.handle(*actions[data_string][1:])
                                
        except Exception as e:
            self.logger.error(f"Error handling input: {traceback.format_exc()}")

        
    def run(self):
        """Main service loop"""
        self.running = True
        config = self.load_config()
        
        self.logger.info("Serial service starting")

        # devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        # for device in devices:
        #     self.logger.info(device.name)
        
        if not self.connect_serial(config):
            self.logger.error("Failed to establish serial connection")
            return 1
            
        try:
            while self.running:
                if self.serial.in_waiting:
                    data = self.serial.readline()
                    self.process_data(data)
                    
                time.sleep(0.01)  # Small delay to prevent CPU spinning
                
        except Exception as e:
            self.logger.error(f"Service error: {e}")
            return 0
        finally:
            self.cleanup()
            
        self.logger.info("Serial service stopped")
        return 0
        
    def cleanup(self):
        """Cleanup resources"""
        if self.serial:
            self.serial.close()
            self.evdev_handler.close()
            
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}")
        self.running = False

if __name__ == "__main__":
    service = SerialService()
    
    # Handle signals
    signal.signal(signal.SIGTERM, service.signal_handler)
    signal.signal(signal.SIGINT, service.signal_handler)
    
    # Run service
    sys.exit(service.run())
