import os
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import argparse
from datetime import datetime
from flask import Flask, request, Response, abort

app = Flask(__name__)

# Path for persistent JSON storage
DATA_FILE = "alpha2_data.json"

# Initialize with default data if no persistence file exists
def init_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    
    # Default data structure based on the example XML
    default_data = {
        "Device": {
            "ID": "EZR010A49",
            "TYPE": "EZRCTRL1",
            "NAME": "EZR010A49",
            "ORIGIN": "EZR010A49",
            "ERRORCOUNT": 0,
            "DATETIME": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "DAYOFWEEK": datetime.now().weekday() + 1,
            "TIMEZONE": 1,
            "NTPTIMESYNC": 1,
            "VERS_SW_STM": "86.19",
            "VERS_SW_ETH": "71.40",
            "VERS_HW": "01",
            "TEMPERATUREUNIT": 0,
            "SUMMERWINTER": 1,
            "TPS": 0,
            "LIMITER": 0,
            "MASTERID": "MASTERID",
            "CHANGEOVER": 0,
            "COOLING": 0,
            "MODE": 0,
            "OPERATIONMODE_ACTOR": 0,
            "ANTIFREEZE": 1,
            "ANTIFREEZE_TEMP": 8.0,
            "FIRSTOPEN_TIME": 10,
            "SMARTSTART": 0,
            "ECO_DIFF": 2.0,
            "ECO_INPUTMODE": 0,
            "ECO_INPUT_STATE": 0,
            "T_HEAT_VACATION": 16.0,
            "VACATION": {
                "VACATION_STATE": 0,
                "START_DATE": "2015-00-00",
                "START_TIME": "12:00:00",
                "END_DATE": "2015-00-00",
                "END_TIME": "12:00:00"
            },
            "NETWORK": {
                "MAC": "38:DE:60:01:1F:DE",
                "DHCP": 1,
                "IPV6ACTIVE": 0,
                "IPV4ACTUAL": "192.168.6.161",
                "IPV4SET": "192.168.100.100",
                "IPV6ACTUAL": "",
                "IPV6SET": "",
                "NETMASKACTUAL": "255.255.248.0",
                "NETMASKSET": "255.255.248.0",
                "DNS": "192.168.3.125",
                "GATEWAY": "192.168.3.4"
            },
            "CLOUD": {
                "USERID": "",
                "PASSWORD": "",
                "M2MSERVERPORT": 55555,
                "M2MLOCALPORT": 54062,
                "M2MHTTPPORT": 54062,
                "M2MHTTPSPORT": 58157,
                "M2MSERVERADDRESS": "www.ezr-cloud1.de",
                "M2MACTIVE": 0,
                "M2MSTATE": "Offline"
            },
            "KWLCTRL": {
                "KWL_CONTROL_VISIBLE": 0,
                "KWL_PRESENT": 0,
                "KWL_CONNECTION": 0,
                "KWL_URL": "---",
                "KWL_PORT": 7777,
                "KWL_STATUS": 0,
                "KWL_FLOWCTRL": 0
            },
            "CODE": {
                "EXPERT": "455A526CCD9936D0"
            },
            "RELAIS": {
                "FUNCTION": 0,
                "RELAIS_LEADTIME": 0,
                "RELAIS_STOPPINGTIME": 0,
                "RELAIS_OPERATIONMODE": 0
            },
            "HEATAREAS": [
                {
                    "nr": 1,
                    "HEATAREA_NAME": "1Kitchen",
                    "HEATAREA_MODE": 1,
                    "T_ACTUAL": 22.6,
                    "T_ACTUAL_EXT": 22.6,
                    "T_TARGET": 28.0,
                    "T_TARGET_BASE": 28.0,
                    "HEATAREA_STATE": 0,
                    "PROGRAM_SOURCE": 0,
                    "PROGRAM_WEEK": 2,
                    "PROGRAM_WEEKEND": 0,
                    "PARTY": 0,
                    "PARTY_REMAININGTIME": 0,
                    "PRESENCE": 0,
                    "T_TARGET_MIN": 5.0,
                    "T_TARGET_MAX": 30.0,
                    "RPM_MOTOR": 0,
                    "OFFSET": 0.0,
                    "T_HEAT_DAY": 21.0,
                    "T_HEAT_NIGHT": 19.0,
                    "T_COOL_DAY": 21.0,
                    "T_COOL_NIGHT": 23.0,
                    "T_FLOOR_DAY": 3.0,
                    "HEATINGSYSTEM": 4,
                    "BLOCK_HC": 0,
                    "ISLOCKED": 0,
                    "LOCK_CODE": "455A52185EC6F38A",
                    "LOCK_AVAILABLE": 0,
                    "LIGHT": 15,
                    "SENSOR_EXT": 0,
                    "T_TARGET_ADJUSTABLE": 1
                },
                {
                    "nr": 2,
                    "HEATAREA_NAME": "2Bath",
                    "HEATAREA_MODE": 1,
                    "T_ACTUAL": 22.8,
                    "T_ACTUAL_EXT": 22.8,
                    "T_TARGET": 21.0,
                    "T_TARGET_BASE": 21.0,
                    "HEATAREA_STATE": 0,
                    "PROGRAM_SOURCE": 0,
                    "PROGRAM_WEEK": 2,
                    "PROGRAM_WEEKEND": 0,
                    "PARTY": 0,
                    "PARTY_REMAININGTIME": 0,
                    "PRESENCE": 0,
                    "T_TARGET_MIN": 5.0,
                    "T_TARGET_MAX": 30.0,
                    "RPM_MOTOR": 0,
                    "OFFSET": 0.0,
                    "T_HEAT_DAY": 21.0,
                    "T_HEAT_NIGHT": 19.0,
                    "T_COOL_DAY": 21.0,
                    "T_COOL_NIGHT": 23.0,
                    "T_FLOOR_DAY": 3.0,
                    "HEATINGSYSTEM": 4,
                    "BLOCK_HC": 0,
                    "ISLOCKED": 0,
                    "LOCK_CODE": "455A528B33F719DB",
                    "LOCK_AVAILABLE": 0,
                    "LIGHT": 15,
                    "SENSOR_EXT": 0,
                    "T_TARGET_ADJUSTABLE": 1
                }
            ],
            "HEATCTRLS": [
                {
                    "nr": 1,
                    "INUSE": 1,
                    "HEATAREA_NR": 1,
                    "ACTOR": 1,
                    "ACTOR_PERCENT": 100,
                    "HEATCTRL_STATE": 1
                },
                {
                    "nr": 2,
                    "INUSE": 1,
                    "HEATAREA_NR": 2,
                    "ACTOR": 0,
                    "ACTOR_PERCENT": 0,
                    "HEATCTRL_STATE": 0
                }
            ],
            "IODEVICES": [
                {
                    "nr": 1,
                    "IODEVICE_TYPE": 0,
                    "IODEVICE_ID": 1,
                    "IODEVICE_VERS_HW": 1,
                    "IODEVICE_VERS_SW": "95.66",
                    "HEATAREA_NR": 1,
                    "SIGNALSTRENGTH": 2,
                    "BATTERY": 2,
                    "IODEVICE_STATE": 0,
                    "IODEVICE_COMERROR": 0,
                    "ISON": 1
                },
                {
                    "nr": 2,
                    "IODEVICE_TYPE": 0,
                    "IODEVICE_ID": 2,
                    "IODEVICE_VERS_HW": 1,
                    "IODEVICE_VERS_SW": "95.66",
                    "HEATAREA_NR": 2,
                    "SIGNALSTRENGTH": 2,
                    "BATTERY": 2,
                    "IODEVICE_STATE": 0,
                    "IODEVICE_COMERROR": 0,
                    "ISON": 1
                }
            ]
        }
    }
    
    # Save the default data to the file
    save_data(default_data)
    return default_data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Helper function to generate XML from data
def generate_xml(data, type_name):
    root = ET.Element("Devices")
    device = ET.SubElement(root, "Device")
    
    # Different XML views based on request type
    if type_name == "static":
        # Full data for static view
        add_elements(device, data["Device"])
    elif type_name == "dynamic":
        # Reduced data set for dynamic view
        dynamic_fields = [
            "ERRORCOUNT", "DATETIME", "DAYOFWEEK", "TIMEZONE", "TPS", "LIMITER",
            "CHANGEOVER", "COOLING", "MODE", "ANTIFREEZE_TEMP", "ECO_INPUT_STATE",
            "T_HEAT_VACATION", "VACATION", "CLOUD", "KWLCTRL"
        ]
        for field in dynamic_fields:
            if field in data["Device"]:
                if isinstance(data["Device"][field], dict):
                    subelem = ET.SubElement(device, field)
                    add_elements(subelem, data["Device"][field])
                else:
                    ET.SubElement(device, field).text = str(data["Device"][field])
        
        # Add HEATAREA, IODEVICE data for dynamic view
        add_array_elements(device, data["Device"]["HEATAREAS"], "HEATAREA", 
                          ["HEATAREA_MODE", "T_ACTUAL", "T_ACTUAL_EXT", "T_TARGET", 
                           "T_TARGET_BASE", "HEATAREA_STATE", "PROGRAM_SOURCE", 
                           "PROGRAM_WEEK", "PROGRAM_WEEKEND", "PARTY", 
                           "PARTY_REMAININGTIME", "PRESENCE", "RPM_MOTOR", 
                           "BLOCK_HC", "ISLOCKED", "LOCK_AVAILABLE", "SENSOR_EXT"])
        
        add_array_elements(device, data["Device"]["IODEVICES"], "IODEVICE", 
                          ["SIGNALSTRENGTH", "BATTERY", "IODEVICE_STATE", 
                           "IODEVICE_COMERROR", "ISON"])
    
    elif type_name == "cyclic":
        # Minimal data set for cyclic view
        cyclic_fields = [
            "DATETIME", "DAYOFWEEK", "TIMEZONE", "TPS", "LIMITER",
            "CHANGEOVER", "COOLING", "ANTIFREEZE_TEMP", "ECO_INPUT_STATE",
            "T_HEAT_VACATION", "VACATION", "CLOUD", "KWLCTRL"
        ]
        for field in cyclic_fields:
            if field in data["Device"]:
                if isinstance(data["Device"][field], dict):
                    subelem = ET.SubElement(device, field)
                    add_elements(subelem, data["Device"][field])
                else:
                    ET.SubElement(device, field).text = str(data["Device"][field])
        
        # Add HEATAREA, IODEVICE data for cyclic view
        add_array_elements(device, data["Device"]["HEATAREAS"], "HEATAREA", 
                          ["HEATAREA_MODE", "T_ACTUAL", "T_ACTUAL_EXT", "T_TARGET", 
                           "T_TARGET_BASE", "HEATAREA_STATE", "PROGRAM_SOURCE", 
                           "PROGRAM_WEEK", "PROGRAM_WEEKEND", "PARTY", 
                           "PARTY_REMAININGTIME", "PRESENCE", "ISLOCKED"])
        
        add_array_elements(device, data["Device"]["IODEVICES"], "IODEVICE", 
                          ["SIGNALSTRENGTH", "BATTERY", "IODEVICE_STATE", 
                           "IODEVICE_COMERROR", "ISON"])
    
    # Convert to string and pretty print
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_elements(parent, data_dict):
    for key, value in data_dict.items():
        if isinstance(value, dict):
            subelem = ET.SubElement(parent, key)
            add_elements(subelem, value)
        elif isinstance(value, list):
            if key in ["HEATAREAS", "HEATCTRLS", "IODEVICES"]:
                # Handle arrays by creating numbered elements
                element_name = key[:-1]  # Remove the 's' to get single element name
                for item in value:
                    subelem = ET.SubElement(parent, element_name, attrib={"nr": str(item["nr"])})
                    for subkey, subvalue in item.items():
                        if subkey != "nr":  # Skip the nr attribute
                            ET.SubElement(subelem, subkey).text = str(subvalue)
        else:
            ET.SubElement(parent, key).text = str(value)

def add_array_elements(parent, array_data, element_name, fields):
    for item in array_data:
        elem = ET.SubElement(parent, element_name, attrib={"nr": str(item["nr"])})
        for field in fields:
            if field in item:
                ET.SubElement(elem, field).text = str(item[field])

# Parse incoming XML commands
def parse_command_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
        command_data = {}
        
        for device in root.findall('Device'):
            # Check for commands
            command = device.find('COMMAND')
            if command is not None:
                command_data['COMMAND'] = command.text
            
            # Check for ID
            device_id = device.find('ID')
            if device_id is not None:
                command_data['ID'] = device_id.text
            
            # Process HEATAREA commands
            for heatarea in device.findall('HEATAREA'):
                nr = heatarea.get('nr')
                if nr:
                    heatarea_data = {}
                    for child in heatarea:
                        heatarea_data[child.tag] = child.text
                    command_data[f'HEATAREA_{nr}'] = heatarea_data
            
            # Process other direct commands
            for direct_command in ['DATETIME', 'COOLING', 'VACATION']:
                elem = device.find(direct_command)
                if elem is not None:
                    if direct_command == 'VACATION':
                        vacation_data = {}
                        for child in elem:
                            vacation_data[child.tag] = child.text
                        command_data['VACATION'] = vacation_data
                    else:
                        command_data[direct_command] = elem.text
            
            # Process RELAIS commands
            relais = device.find('RELAIS')
            if relais is not None:
                relais_data = {}
                for child in relais:
                    relais_data[child.tag] = child.text
                command_data['RELAIS'] = relais_data
        
        return command_data
    except Exception as e:
        app.logger.error(f"Error parsing XML command: {str(e)}")
        return None

# Apply commands to update the system state
def apply_command(data, command_data):
    if 'COMMAND' in command_data:
        # Handle special commands (CREATE_XMLDEVICE, CONNECT_XMLDEVICE, etc.)
        command = command_data['COMMAND']
        if command.startswith('CMD_CREATE_XMLDEVICE:'):
            # Extract heat areas from command
            heat_areas = command.split(':')[1].split(',')
            
            # Find next available IODEVICE_ID
            max_id = 0
            for device in data["Device"]["IODEVICES"]:
                if device["IODEVICE_ID"] > max_id:
                    max_id = device["IODEVICE_ID"]
            
            new_id = max_id + 1
            
            # Create virtual room
            new_device = {
                "nr": len(data["Device"]["IODEVICES"]) + 1,
                "IODEVICE_TYPE": 8,  # Virtual room type
                "IODEVICE_ID": new_id,
                "IODEVICE_VERS_HW": 0,
                "IODEVICE_VERS_SW": "00.00",
                "HEATAREA_NR": int(heat_areas[0]),
                "SIGNALSTRENGTH": 2,
                "BATTERY": 0,
                "IODEVICE_STATE": 0,
                "IODEVICE_COMERROR": 0,
                "ISON": 1
            }
            
            data["Device"]["IODEVICES"].append(new_device)
            app.logger.info(f"Created virtual room with ID {new_id}")
        
        elif command.startswith('CMD_CONNECT_XMLDEVICE:'):
            # Connect virtual room to heat areas
            parts = command.split(':')[1].split(',')
            device_id = int(parts[0])
            heat_areas = [int(area) for area in parts[1:]]
            
            # Find the device
            for device in data["Device"]["IODEVICES"]:
                if device["IODEVICE_ID"] == device_id:
                    device["HEATAREA_NR"] = heat_areas[0]  # Update primary heat area
                    app.logger.info(f"Connected device {device_id} to heat areas {heat_areas}")
                    break
        
        elif command.startswith('CMD_DELETE_XMLDEVICE:'):
            # Delete virtual room
            device_id = int(command.split(':')[1])
            
            # Remove the device
            data["Device"]["IODEVICES"] = [
                device for device in data["Device"]["IODEVICES"] 
                if device["IODEVICE_ID"] != device_id
            ]
            app.logger.info(f"Deleted device {device_id}")
    
    # Handle direct property updates
    if 'ID' in command_data:
        device_id = command_data['ID']
        if device_id == data["Device"]["ID"]:
            # Process DATETIME update
            if 'DATETIME' in command_data:
                data["Device"]["DATETIME"] = command_data['DATETIME']
                app.logger.info(f"Updated DATETIME to {command_data['DATETIME']}")
            
            # Process COOLING update
            if 'COOLING' in command_data:
                data["Device"]["COOLING"] = int(command_data['COOLING'])
                app.logger.info(f"Updated COOLING to {command_data['COOLING']}")
            
            # Process VACATION update
            if 'VACATION' in command_data:
                for key, value in command_data['VACATION'].items():
                    data["Device"]["VACATION"][key] = value
                app.logger.info("Updated VACATION settings")
            
            # Process RELAIS update
            if 'RELAIS' in command_data:
                for key, value in command_data['RELAIS'].items():
                    data["Device"]["RELAIS"][key] = int(value) if value.isdigit() else value
                app.logger.info("Updated RELAIS settings")
            
            # Process HEATAREA updates
            for key, value in command_data.items():
                if key.startswith('HEATAREA_'):
                    area_nr = int(key.split('_')[1])
                    # Find the heat area
                    for area in data["Device"]["HEATAREAS"]:
                        if area["nr"] == area_nr:
                            for subkey, subvalue in value.items():
                                # Convert to appropriate type
                                if subkey in ['T_TARGET', 'T_ACTUAL']:
                                    area[subkey] = float(subvalue)
                                elif subkey in ['HEATAREA_MODE', 'ISLOCKED']:
                                    area[subkey] = int(subvalue)
                                else:
                                    area[subkey] = subvalue
                            app.logger.info(f"Updated HEATAREA {area_nr}")
                            break
    
    return data

# Flask routes
@app.route('/data/static.xml', methods=['GET'])
def get_static_xml():
    data = init_data()
    xml_content = generate_xml(data, "static")
    return Response(xml_content, mimetype='application/xml')

@app.route('/data/dynamic.xml', methods=['GET'])
def get_dynamic_xml():
    data = init_data()
    xml_content = generate_xml(data, "dynamic")
    return Response(xml_content, mimetype='application/xml')

@app.route('/data/cyclic.xml', methods=['GET'])
def get_cyclic_xml():
    data = init_data()
    # Update date and time for cyclic updates
    data["Device"]["DATETIME"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    data["Device"]["DAYOFWEEK"] = datetime.now().weekday() + 1
    save_data(data)
    
    xml_content = generate_xml(data, "cyclic")
    return Response(xml_content, mimetype='application/xml')

@app.route('/data/changes.xml', methods=['POST'])
def post_changes():
    if not request.data:
        app.logger.warning("No XML data provided")
        abort(400, description="No XML data provided")
    
    xml_data = request.data.decode('utf-8')
    command_data = parse_command_xml(xml_data)
    
    if not command_data:
        app.logger.warning("Invalid XML command format")
        abort(400, description="Invalid XML command format")
    
    data = init_data()
    updated_data = apply_command(data, command_data)
    save_data(updated_data)
    
    # Return success response
    response_xml = '<?xml version="1.0" encoding="UTF-8"?><response><status>OK</status></response>'
    return Response(response_xml, mimetype='application/xml')

def parse_args():
    """Parse command line arguments."""
    # Default values
    default_host = "0.0.0.0"
    default_port = 5000
    default_debug = False
    default_data_file = "alpha2_data.json"
    
    # Check for environment variables
    env_host = os.environ.get("ALPHA2_HOST", default_host)
    env_port = int(os.environ.get("ALPHA2_PORT", default_port))
    env_debug = os.environ.get("ALPHA2_DEBUG", "").lower() in ("true", "1", "yes")
    env_data_file = os.environ.get("ALPHA2_DATA_FILE", default_data_file)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Alpha 2 XML API Mock Server')
    parser.add_argument('--host', type=str, default=env_host,
                        help=f'Host to bind the server to (default: {env_host})')
    parser.add_argument('--port', type=int, default=env_port,
                        help=f'Port to bind the server to (default: {env_port})')
    parser.add_argument('--debug', action='store_true', default=env_debug,
                        help='Enable debug mode')
    parser.add_argument('--data-file', type=str, default=env_data_file,
                        help=f'Path to the data file (default: {env_data_file})')
    
    args = parser.parse_args()
    
    # Update global data file path
    global DATA_FILE
    DATA_FILE = args.data_file
    
    return args

if __name__ == '__main__':
    # Parse configuration
    args = parse_args()
    
    # Print configuration
    print(f"Starting Alpha 2 Mock Server:")
    print(f"  Host: {args.host}")
    print(f"  Port: {args.port}")
    print(f"  Debug: {args.debug}")
    print(f"  Data file: {DATA_FILE}")
    
    # Ensure we have initial data
    init_data()
    
    # Run the server
    app.run(host=args.host, port=args.port, debug=args.debug)