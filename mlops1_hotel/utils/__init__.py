from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="HOTEL-RESERVATION-PROJECT",
    version="0.1",
    author="Simran R",
    packages=find_packages(),
    install_requires= requirements,
    )
# Run this command for running setup file : 
# pip istall -e .