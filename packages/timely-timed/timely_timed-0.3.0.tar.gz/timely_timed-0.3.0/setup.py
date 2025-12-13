from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="timely-timed",
    version="0.3.0",
    author="Mike Berensmeier",
    author_email="berensmeier.mike@keemail.me",
    description="A Python package for fetching UTC time from multiple time servers with fallback logic. Features free servers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/lorrooar/timely-timed",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    python_requires=">=3.8",
    keywords="time, utc, datetime, http, api",
)