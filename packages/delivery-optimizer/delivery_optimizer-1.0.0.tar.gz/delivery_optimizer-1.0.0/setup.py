from setuptools import setup, find_packages
import os

# Read the README file
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="delivery-optimizer",
    version="1.0.0",
    author="Abhishek Sharma",
    author_email="abhishekmsharma21@gmail.com",
    description="A Python library for calculating delivery distances and pricing using the Haversine formula",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbhishekSharmaIE/courier-delivery-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
    keywords="delivery, distance, haversine, pricing, courier, logistics, geolocation",
    project_urls={
        "Bug Reports": "https://github.com/AbhishekSharmaIE/courier-delivery-system/issues",
        "Source": "https://github.com/AbhishekSharmaIE/courier-delivery-system",
        "Documentation": "https://github.com/AbhishekSharmaIE/courier-delivery-system#readme",
    },
)

