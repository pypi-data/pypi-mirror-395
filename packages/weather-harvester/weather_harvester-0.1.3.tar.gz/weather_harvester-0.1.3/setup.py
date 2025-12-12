from setuptools import setup, find_packages

setup(
    name="weather_harvester",
    version="0.1.3",
    description="Weather Data Harvester with caching, alerts, CLI, and exports",
    author="Your Name",
    packages=find_packages(),  # auto-detects weather_harvester package
    include_package_data=True,
    install_requires=[
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "weather-harvester = weather_harvester.main:main",
        ]
    },
)
