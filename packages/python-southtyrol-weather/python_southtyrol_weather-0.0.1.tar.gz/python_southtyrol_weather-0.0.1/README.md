# python-southtyrol-weather
Python library that provides real-time and forecast weather for southtyrol using the [Open Data Hub API](https://opendatahub.com).

## Features

- Get metadata for all available stations

- Find nearby stations

- Fetch latest measurement for each station

## Installation

Install via pip:

```bash
pip install python-southtyrol-weather
```

> Requires Python 3.10 or higher

## Dependencies

- aiohttp 3.11 or higher

## Usage Example

```python
async def main():   
    async with ClientSession() as session:
        stations = await fetchStations(session)
        print(stations)
        measurement = await fetchMeasurement(session, stations[0].id)
        print(measurement)
```

## License

MIT License

## Contributing

Contributions are welcome!\
Feel free to open issues, submit pull requests, or suggest features.


