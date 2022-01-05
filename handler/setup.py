"""
Build and installation information for Ganesha Request Handler
"""

from setuptools import setup, find_packages

setup(
    name='grh',
    version='0.1',
    description="http server that serves Ganesha Request Handler requests",
    packages=find_packages(exclude=["tests"]),
    entry_points={
        'console_scripts': [
            "grh_handler = handler.app:main",
        ],
    },
    python_requires='>=3.6',
)
