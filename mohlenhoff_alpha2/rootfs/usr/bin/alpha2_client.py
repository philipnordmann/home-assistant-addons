import requests
import logging
import xml.etree.ElementTree as ET


class Alpha2Client:
    def __init__(self, host):
        self.host = host
        self.api_url = f"http://{host}/data/changes.xml"
        self.static_url = f"http://{host}/data/static.xml"
        self.logger = logging.getLogger(__name__)
        self.device_id = self._get_device_id()

    def _get_device_id(self):
        
        content = self._get_static()

        if content:
            root = ET.fromstring(content)       
            device_id = root.find('./Device/ID').text
            return device_id
        
    def create_virtual_device(self, area_id):
        """Create a virtual device in the Alpha 2 system"""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Devices>
            <Device>
                <COMMAND>CMD_CREATE_XMLDEVICE:{area_id}</COMMAND>
            </Device>
        </Devices>"""
        
        return self._send_command(xml)
    
    def update_temperature(self, area_id, temperature):
        """Update the actual temperature for a heating area"""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Devices>
            <Device>
                <ID>{self.device_id}</ID>
                <HEATAREA nr="{area_id}">
                    <T_ACTUAL>{temperature}</T_ACTUAL>
                </HEATAREA>
            </Device>
        </Devices>"""
        
        return self._send_command(xml)
        
    def set_target_temperature(self, area_id, temperature):
        """Set the target temperature for a heating area"""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Devices>
            <Device>
                <ID>{self.device_id}</ID>
                <HEATAREA nr="{area_id}">
                    <T_TARGET>{temperature}</T_TARGET>
                </HEATAREA>
            </Device>
        </Devices>"""
        
        return self._send_command(xml)
    
    def get_all_devices(self):
        content = self._get_static()

        if content:
            root = ET.fromstring(content)
            iodevices = []
            
            # Find all IODEVICE elements
            for iodevice_elem in root.findall('./Device/IODEVICE'):
                # Get the 'nr' attribute
                device_nr = iodevice_elem.get('nr')
                
                # Create dictionary for this IODEVICE
                iodevice = {'nr': device_nr}
                
                # Add all child elements to the dictionary
                for child in iodevice_elem:
                    iodevice[child.tag] = child.text
                
                iodevices.append(iodevice)
            
            return iodevices
    
    def _get_static(self):
        try:
            headers = {'Content-Type': 'application/xml'}
            response = requests.get(self.static_url, headers=headers)
            
            if response.status_code == 200:
                return response.content
            else:
                self.logger.error(f"Failed get static.xml: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Error communicating with Alpha 2: {e}")
            return None

    def _send_command(self, xml_data):
        try:
            headers = {'Content-Type': 'application/xml'}
            response = requests.post(self.api_url, data=xml_data, headers=headers)
            
            if response.status_code == 200:
                self.logger.info("Command sent successfully")
                return True
            else:
                self.logger.error(f"Failed to send command: {response.status_code}, {response.text}")
                return False
        except Exception as e:
            self.logger.error(f"Error communicating with Alpha 2: {e}")
            return False