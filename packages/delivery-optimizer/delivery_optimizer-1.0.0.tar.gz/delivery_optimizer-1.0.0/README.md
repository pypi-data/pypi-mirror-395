# Delivery Optimizer

A Python library for calculating delivery distances and pricing using the Haversine formula.

## Features

- **Distance Calculation**: Calculate the great-circle distance between two geographical locations using the Haversine formula
- **Pricing Engine**: Calculate delivery pricing based on distance and weight
- **Location Management**: Simple Location class for managing geographical coordinates
- **Customizable**: Configurable pricing parameters

## Installation

```bash
pip install delivery-optimizer
```

## Quick Start

```python
from delivery_optimizer import Location, DistanceCalculator, PricingEngine

# Create locations
pickup = Location(53.3498, -6.2603, "Dublin, Ireland")
delivery = Location(53.4129, -8.2439, "Galway, Ireland")

# Calculate distance
distance = DistanceCalculator.calculate(pickup, delivery)
print(f"Distance: {distance} km")  # Distance: 208.42 km

# Calculate price
pricing = PricingEngine()
price = pricing.calculate(distance, weight_kg=2.5)
print(f"Price: ${price}")  # Price: $528.55
```

## Usage

### Location

The `Location` class represents a geographical location:

```python
from delivery_optimizer import Location

location = Location(
    latitude=53.3498,
    longitude=-6.2603,
    address="Dublin, Ireland"
)
```

### Distance Calculation

Calculate the distance between two locations:

```python
from delivery_optimizer import Location, DistanceCalculator

location1 = Location(53.3498, -6.2603)
location2 = Location(53.4129, -8.2439)

distance_km = DistanceCalculator.calculate(location1, location2)
print(f"Distance: {distance_km} km")
```

### Pricing

Calculate delivery pricing:

```python
from delivery_optimizer import PricingEngine

# Default pricing
pricing = PricingEngine()
price = pricing.calculate(distance_km=100, weight_kg=2.5)

# Custom pricing
custom_pricing = PricingEngine(
    base_price=10.0,
    price_per_km=3.0,
    price_per_kg=1.5
)
price = custom_pricing.calculate(distance_km=100, weight_kg=2.5)
```

## Pricing Formula

The default pricing formula is:

```
price = base_price + (distance_km × price_per_km) + (weight_kg × price_per_kg)
```

Default values:
- Base price: $5.0
- Price per km: $2.5
- Price per kg: $1.0

## API Reference

### Location

```python
Location(latitude: float, longitude: float, address: str = "")
```

### DistanceCalculator

```python
DistanceCalculator.calculate(location1: Location, location2: Location) -> float
```

Returns distance in kilometers (rounded to 2 decimal places).

### PricingEngine

```python
PricingEngine(base_price: float = None, price_per_km: float = None, price_per_kg: float = None)
pricing.calculate(distance_km: float, weight_kg: float = 1.0) -> float
```

Returns price rounded to 2 decimal places.

## Requirements

- Python 3.8+

## License

MIT License

## Author

Abhishek Sharma

## Links

- GitHub: https://github.com/AbhishekSharmaIE/courier-delivery-system
- PyPI: https://pypi.org/project/delivery-optimizer/

