# Elli Client

Python client library for the Elli Wallbox API.

## Installation

```bash
pip install elli-client
```

## Quick Start

```python
from elli_client import ElliAPIClient

# Initialize client and login
client = ElliAPIClient()
token = client.login("your.email@example.com", "your_password")

# Get charging stations
stations = client.get_stations()
for station in stations:
    print(f"Station: {station.name} ({station.id})")

# Get active charging session
session = client.get_active_charging_session()
if session:
    print(f"Charging: {session.energy_consumption_wh / 1000:.2f} kWh")
    print(f"Power: {session.momentary_power_w} W")
```

## Features

- Authentication with Elli Account
- Query charging stations
- Retrieve charging sessions (active and historical)
- Current charging power and energy consumption
- Station information

## Documentation

- **[Quick Start Guide](docs/quick-start.md)** - Get started in minutes
- **[API Reference](docs/api.md)** - Complete API documentation
- **[Docs Overview](docs/README.md)** - Documentation index

## Development

### Setup

```bash
git clone https://github.com/marcszy91/elli-client
cd elli-client
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Copy environment template and add your credentials
cp .env.template .env
# Edit .env and add your ELLI_EMAIL and ELLI_PASSWORD
```

### Testing

```bash
# Format code
black src/
isort src/

# Run tests (when implemented)
pytest
```

## Home Assistant Integration

This client is used by the [Elli Charger HACS integration](https://github.com/marcszy91/hacs-elli-charger) for Home Assistant.

## License

MIT License - see LICENSE file for details

## Disclaimer

This library was created through reverse engineering of the official Elli iPhone app. It is not officially supported by Elli or Volkswagen Group Charging GmbH. Use at your own risk.
