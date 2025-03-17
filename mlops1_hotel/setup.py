from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-1-RESERVATION",
    version="0.1",
    author="Simran",
    packages=find_packages(),
    install_requires = requirements,
)

# To run setup file(Install all packages) :
# RUN : "pip install -e ."
# It creates a .egg folder with all metadat of packages.