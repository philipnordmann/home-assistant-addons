#!/usr/bin/env python3
import os
import json
import time
import logging
import requests
from alpha2_client import Alpha2Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('alpha2-integration')

class Alpha2Integration:
    def __init__(self):
        # Load configuration from environment or file
        self.load_config()
        
        # Initialize Alpha 2 client
        self.alpha2 = Alpha2Client(self.config['alpha2_host'])
        
        # Home Assistant API settings
        self.ha_url = os.environ.get('SUPERVISOR_URL', 'http://supervisor/core')
        self.ha_token = os.environ.get('SUPERVISOR_TOKEN', '')
        self.ha_headers = {
            'Authorization': f'Bearer {self.ha_token}',
            'Content-Type': 'application/json',
        }
    
    def load_config(self):
        """Load configuration from options.json or environment"""
        # Try to load from file first
        config_path = '/data/options.json'
        if os.path.exists(config_path):
            with open(config_path) as f:
                self.config = json.load(f)
                logger.info("Loaded configuration from options.json")
        else:
            # Fall back to environment variables for testing
            self.config = {
                'alpha2_host': os.environ.get('ALPHA2_HOST', 'localhost:5000'),
                'update_interval': int(os.environ.get('UPDATE_INTERVAL', '60')),
                'virtual_devices': json.loads(os.environ.get('VIRTUAL_DEVICES', '[]'))
            }
            logger.info("Loaded configuration from environment variables")
    
    def start(self):
        """Start the integration"""
        last_config_mtime = 0
        config_path = '/data/options.json'
        
        while True:
            try:
                # Check if config has been updated
                if os.path.exists(config_path):
                    current_mtime = os.path.getmtime(config_path)
                    if current_mtime > last_config_mtime:
                        logger.info("Configuration changed, reloading...")
                        self.load_config()
                        self.setup_virtual_devices()
                        last_config_mtime = current_mtime
                
                # Update temperatures
                self.update_temperatures()
                
                # Wait before next check
                time.sleep(self.config['update_interval'])
            except KeyboardInterrupt:
                logger.info("Stopping integration...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)  # Wait before retry
    
    def setup_virtual_devices(self):
        """Create virtual devices in Alpha 2"""
        for device in self.config['virtual_devices']:
            # Create virtual device in Alpha 2
            logger.info(f"Creating virtual device: {device['name']} (AREA: {device['area_id']})")
            devices = self.alpha2.get_all_devices()
            virt_rooms = [elem["HEATAREA_NR"] for elem in devices if elem["IODEVICE_TYPE"] == "8"]
            if str(device['area_id']) in virt_rooms:
                logger.info(f"Skipping device for area {device['area_id']}, device already present")
                continue

            result = self.alpha2.create_virtual_device(device['area_id'])
            if not result:
                logger.error(f"Failed to create device {device['name']} in Alpha 2")
                continue
            
            logger.info(f"Created virtual device {device['name']} in Alpha 2")
    
    def update_temperatures(self):
        """Update temperature values for all virtual devices"""
        for device in self.config['virtual_devices']:
            # Get current temperature from sensor via Home Assistant API
            entity_id = device['temperature_entity_id']
            logger.debug(f"Fetching temperature from {entity_id}")
            
            try:
                response = requests.get(
                    f"{self.ha_url}/api/states/{entity_id}",
                    headers=self.ha_headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Handle different sensor formats
                    if data['state'] == 'unavailable' or data['state'] == 'unknown':
                        logger.warning(f"Sensor {entity_id} is {data['state']}")
                        continue
                        
                    try:
                        # Try to get temperature directly from state
                        current_temp = float(data['state'])
                    except ValueError:
                        # If state isn't a number, try to get it from attributes
                        if 'attributes' in data and 'temperature' in data['attributes']:
                            current_temp = float(data['attributes']['temperature'])
                        else:
                            logger.error(f"Could not extract temperature from {entity_id}")
                            continue
                    
                    area_id = device['area_id']
                    
                    # Update Alpha 2 with current temperature
                    logger.info(f"Updating {device['name']} with temperature {current_temp}")
                    self.alpha2.update_temperature(area_id, current_temp)
                    
                else:
                    logger.error(f"Failed to get temperature for {entity_id}: {response.status_code}")
            except Exception as e:
                logger.error(f"Error getting temperature for {entity_id}: {e}")

if __name__ == "__main__":
    integration = Alpha2Integration()
    integration.start()