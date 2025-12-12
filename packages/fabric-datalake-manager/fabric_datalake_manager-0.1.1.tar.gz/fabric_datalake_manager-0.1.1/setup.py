from setuptools import setup, find_packages
from pathlib import Path

# Read README.md using UTF-8 to avoid Windows cp1252 decoding errors
long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name='fabric_datalake_manager',
    version='0.1.1',
    description='A Fabric extension for managing data lakes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mahmudul Hasan Roni',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        "dacite>=1.9.2",
    ],
)
