# Möhlenhoff Alpha 2 Home Assistant Add-on

![Aarch64][aarch64-shield] ![AMD64][amd64-shield] ![ARMHF][armhf-shield] ![ARMv7][armv7-shield] ![i386][i386-shield]

Integrate Möhlenhoff Alpha 2 heating systems with Home Assistant, allowing you to use any Home Assistant temperature sensor to control your heating zones.

## About

The Möhlenhoff Alpha 2 is a popular heating control system for underfloor heating and radiators. This add-on creates a bridge between your Alpha 2 system and Home Assistant, enabling you to use any temperature sensor in Home Assistant to control your heating zones.

### Key Features

- Creates virtual rooms in your Alpha 2 system
- Sends temperature readings from any Home Assistant sensor to your Alpha 2 controller
- Uses the Alpha 2 XML API for communication
- Automatic temperature synchronization at configurable intervals
- Works with any temperature sensor in Home Assistant (including Zigbee, Z-Wave, WiFi, and other sensors)

## Installation

1. Add this repository to your Home Assistant instance
2. Install the "Möhlenhoff Alpha 2 Add-on" from the add-on store
3. Configure the add-on (see configuration below)
4. Start the add-on

## Configuration

```yaml
alpha2_host: "192.168.1.100"
update_interval: 60
virtual_devices:
  - name: "Living Room"
    area_id: 1
    temperature_entity_id: "sensor.living_room_temperature"
  - name: "Bedroom"
    area_id: 2
    temperature_entity_id: "sensor.bedroom_temperature"
```

### Configuration Options

| Option | Description |
|--------|-------------|
| `alpha2_host` | IP address and port (if not default) of your Alpha 2 base station (e.g., "192.168.1.100" or "192.168.1.100:5000") |
| `update_interval` | How often to update temperatures (in seconds, range: 10-600) |
| `virtual_devices` | List of virtual rooms to create |

Each virtual device requires:
- `name`: Friendly name for the room
- `area_id`: Heating area ID in Alpha 2 system (1-255)
- `temperature_entity_id`: Home Assistant entity ID of temperature sensor

## How It Works

The add-on communicates with your Alpha 2 base station using its XML API. When started, it:

1. Creates virtual devices in the Alpha 2 system for each configured room
2. Periodically retrieves temperature readings from the specified Home Assistant sensors
3. Updates the Alpha 2 system with these temperature values
4. The Alpha 2 system then controls your heating based on these values and your configured setpoints

This allows you to use any temperature sensor in Home Assistant instead of being limited to the Alpha 2's own room controllers.

## Troubleshooting

Check the add-on logs for any error messages. Common issues include:

- Incorrect Alpha 2 host IP address
- Invalid temperature entity ID
- Network connectivity issues between Home Assistant and Alpha 2
- Alpha 2 system not supporting the XML API (check your firmware version)

## Support

If you have any questions or need help, please [open an issue](https://github.com/philipnordmann/mohlenhoff_alpha2/issues) on GitHub.

## License

MIT License

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg