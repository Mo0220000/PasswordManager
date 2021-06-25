from setuptools import setup

setup(
    name="pasman",
    packages=["pasman"],
    entry_points = {
        "console_scripts": [
            "pasman = pasman.Main:main",
        ]
    }
)