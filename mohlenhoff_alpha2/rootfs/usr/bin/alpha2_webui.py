#!/usr/bin/env python3
import os
import json
import logging
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from alpha2_client import Alpha2Client
from werkzeug.middleware.proxy_fix import ProxyFix


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('alpha2-webui')

app = Flask(__name__, 
            static_folder='/usr/share/alpha2/static',
            template_folder='/usr/share/alpha2/templates')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

ingress_path = os.environ.get('INGRESS_URI', '')
app.config['APPLICATION_ROOT'] = ingress_path

def load_config():
    """Load configuration from options.json"""
    config_path = '/data/options.json'
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {
        'alpha2_host': os.environ.get('ALPHA2_HOST', 'localhost:5000'),
        'update_interval': int(os.environ.get('UPDATE_INTERVAL', '60')),
        'virtual_devices': []
    }

def save_config(config):
    """Save configuration to options.json"""
    with open('/data/options.json', 'w') as f:
        json.dump(config, f, indent=2)

def get_ha_sensors():
    """Get temperature sensors from Home Assistant"""
    ha_url = os.environ.get('SUPERVISOR_URL', 'http://supervisor/core')
    ha_token = os.environ.get('SUPERVISOR_TOKEN', '')
    ha_headers = {
        'Authorization': f'Bearer {ha_token}',
        'Content-Type': 'application/json',
    }
    
    try:
        # Get all entities
        response = requests.get(
            f"{ha_url}/api/states",
            headers=ha_headers,
            timeout=10
        )
        
        if response.status_code == 200:
            all_entities = response.json()
            
            # Filter for temperature sensors
            temp_sensors = []
            for entity in all_entities:
                entity_id = entity['entity_id']
                
                # Check if it's a temperature sensor
                is_temp_sensor = False
                
                # Check entity domain
                if entity_id.startswith('sensor.') or entity_id.startswith('climate.'):
                    # Check attributes for temperature
                    if 'attributes' in entity and 'unit_of_measurement' in entity['attributes']:
                        if entity['attributes']['unit_of_measurement'] in ['°C', '°F', 'K']:
                            is_temp_sensor = True
                    
                    # Try to parse state as float (might be temperature)
                    try:
                        float(entity['state'])
                        # If device class exists and is temperature
                        if 'attributes' in entity and 'device_class' in entity['attributes']:
                            if entity['attributes']['device_class'] == 'temperature':
                                is_temp_sensor = True
                    except (ValueError, TypeError):
                        pass
                
                if is_temp_sensor:
                    friendly_name = entity.get('attributes', {}).get('friendly_name', entity_id)
                    temp_sensors.append({
                        'entity_id': entity_id,
                        'name': friendly_name,
                        'state': entity['state'],
                        'unit': entity.get('attributes', {}).get('unit_of_measurement', '')
                    })
            
            return temp_sensors
        else:
            logger.error(f"Failed to get entities: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error getting entities: {e}")
        return []

@app.route(f'{ingress_path}/')
def index():
    """Main dashboard page"""
    config = load_config()
    return render_template('index.html', 
                          config=config,
                          virtual_devices=config['virtual_devices'])

@app.route(f'{ingress_path}/rooms')
def rooms():
    """Manage virtual rooms page"""
    config = load_config()
    alpha2 = Alpha2Client(config['alpha2_host'])
    
    # Get available temperature sensors
    temp_sensors = get_ha_sensors()
    
    # Get all devices from Alpha 2
    alpha2_devices = alpha2.get_all_devices()
    
    return render_template('rooms.html',
                          config=config,
                          virtual_devices=config['virtual_devices'],
                          temp_sensors=temp_sensors,
                          alpha2_devices=alpha2_devices)

@app.route(f'{ingress_path}/api/rooms', methods=['GET'])
def get_rooms():
    """API endpoint to get all virtual rooms"""
    config = load_config()
    return jsonify(config['virtual_devices'])

@app.route(f'{ingress_path}/api/rooms/add', methods=['POST'])
def add_room():
    """API endpoint to add a new virtual room"""
    config = load_config()
    
    data = request.form
    name = data.get('name')
    area_id = int(data.get('area_id'))
    temperature_entity_id = data.get('temperature_entity_id')
    
    # Validate inputs
    if not name or not area_id or not temperature_entity_id:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    # Check for duplicate area_id
    for device in config['virtual_devices']:
        if device['area_id'] == area_id:
            return jsonify({'success': False, 'message': f'Area ID {area_id} already in use'}), 400
    
    # Add new device
    new_device = {
        'name': name,
        'area_id': area_id,
        'temperature_entity_id': temperature_entity_id
    }
    
    config['virtual_devices'].append(new_device)
    save_config(config)
    
    # Create virtual device in Alpha 2
    alpha2 = Alpha2Client(config['alpha2_host'])
    result = alpha2.create_virtual_device(area_id)
    
    if result:
        return jsonify({'success': True, 'message': 'Room added successfully'})
    else:
        # Revert config change if API call failed
        config['virtual_devices'].pop()
        save_config(config)
        return jsonify({'success': False, 'message': 'Failed to create room in Alpha 2'}), 500

@app.route(f'{ingress_path}/api/rooms/delete/<int:area_id>', methods=['POST'])
def delete_room(area_id):
    """API endpoint to delete a virtual room"""
    config = load_config()
    
    # Find the device with the given area_id
    for i, device in enumerate(config['virtual_devices']):
        if device['area_id'] == area_id:
            # Remove from config
            del config['virtual_devices'][i]
            save_config(config)
            
            # TODO: Implement deletion from Alpha 2 if needed
            
            return jsonify({'success': True, 'message': 'Room deleted successfully'})
    
    return jsonify({'success': False, 'message': 'Room not found'}), 404

@app.route(f'{ingress_path}/api/sensors', methods=['GET'])
def get_sensors():
    """API endpoint to get all temperature sensors"""
    sensors = get_ha_sensors()
    return jsonify(sensors)

if __name__ == '__main__':
    # Get ingress port from environment
    ingress_port = int(os.environ.get('INGRESS_PORT', 8099))
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=ingress_port)