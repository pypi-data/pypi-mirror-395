"""
Delivery Optimizer - Core functionality for distance and pricing calculations.
"""

import math


class Location:
    """Represents a geographical location with latitude and longitude."""
    
    def __init__(self, latitude: float, longitude: float, address: str = ""):
        """
        Initialize a Location object.
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            address: Optional address string
        """
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
    
    def __repr__(self):
        return f"Location(lat={self.latitude}, lon={self.longitude}, address='{self.address}')"


class DistanceCalculator:
    """Calculates distance between two locations using the Haversine formula."""
    
    EARTH_RADIUS_KM = 6371.0
    
    @staticmethod
    def calculate(location1: Location, location2: Location) -> float:
        """
        Calculate the great-circle distance between two locations in kilometers.
        
        Uses the Haversine formula to calculate the shortest distance
        between two points on a sphere.
        
        Args:
            location1: First location
            location2: Second location
            
        Returns:
            Distance in kilometers (rounded to 2 decimal places)
        """
        lat1_rad = math.radians(location1.latitude)
        lat2_rad = math.radians(location2.latitude)
        delta_lat = math.radians(location2.latitude - location1.latitude)
        delta_lon = math.radians(location2.longitude - location1.longitude)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = DistanceCalculator.EARTH_RADIUS_KM * c
        return round(distance, 2)


class PricingEngine:
    """Calculates delivery pricing based on distance and weight."""
    
    BASE_PRICE = 5.0  # Base price in currency units
    PRICE_PER_KM = 2.5  # Price per kilometer
    PRICE_PER_KG = 1.0  # Price per kilogram
    
    def __init__(self, base_price: float = None, price_per_km: float = None, 
                 price_per_kg: float = None):
        """
        Initialize PricingEngine with custom pricing parameters.
        
        Args:
            base_price: Base delivery price (default: 5.0)
            price_per_km: Price per kilometer (default: 2.5)
            price_per_kg: Price per kilogram (default: 1.0)
        """
        self.base_price = base_price or PricingEngine.BASE_PRICE
        self.price_per_km = price_per_km or PricingEngine.PRICE_PER_KM
        self.price_per_kg = price_per_kg or PricingEngine.PRICE_PER_KG
    
    def calculate(self, distance_km: float, weight_kg: float = 1.0) -> float:
        """
        Calculate delivery price based on distance and weight.
        
        Formula: base_price + (distance * price_per_km) + (weight * price_per_kg)
        
        Args:
            distance_km: Distance in kilometers
            weight_kg: Weight in kilograms (default: 1.0)
            
        Returns:
            Total price rounded to 2 decimal places
        """
        price = (self.base_price + 
                (distance_km * self.price_per_km) + 
                (weight_kg * self.price_per_kg))
        return round(price, 2)

