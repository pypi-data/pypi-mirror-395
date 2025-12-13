from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agnipod",
    version="0.1.0",
    author="Anuj Sangwan",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "agnipod=agnipod.main:hello",
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)