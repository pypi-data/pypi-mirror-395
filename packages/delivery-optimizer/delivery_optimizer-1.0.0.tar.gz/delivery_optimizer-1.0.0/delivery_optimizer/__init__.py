"""
Delivery Optimizer - A Python library for calculating delivery distances and pricing.

This library provides tools for:
- Calculating distances between locations using the Haversine formula
- Calculating delivery pricing based on distance and weight
- Location management for delivery systems
"""

from .optimizer import Location, DistanceCalculator, PricingEngine

__version__ = "1.0.0"
__author__ = "Abhishek Sharma"
__email__ = "abhishekmsharma21@gmail.com"

__all__ = ["Location", "DistanceCalculator", "PricingEngine"]

