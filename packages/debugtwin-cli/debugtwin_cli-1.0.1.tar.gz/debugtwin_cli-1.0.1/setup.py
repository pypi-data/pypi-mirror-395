from setuptools import setup, find_packages

setup(
    name="debugtwin-cli",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "aiohttp>=3.8.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "debugtwin=debugtwin_cli.main:cli",
        ],
    },
)
