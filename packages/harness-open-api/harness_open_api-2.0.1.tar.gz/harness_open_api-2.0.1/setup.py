import os
from setuptools import setup, find_packages

setup(
    name='harness-open-api',  # Change to a unique name
    version=os.getenv('PACKAGE_VERSION'),
    description='Harness NextGen Software Delivery Platform API Reference',
    author='Harness Solutions Factory',
    author_email='hsf-team@harness.io',
    packages=find_packages(where="src"),
    package_dir={"": "src"},  # This tells setuptools where to find packages
    install_requires=[
        'certifi>=14.05.14',
        'six>=1.10',
        'python_dateutil>=2.5.3',
        'setuptools>=70.0.0',
        'urllib3>=1.15.1'
    ],       # Add dependencies if needed
    python_requires='>=3.9',
)

