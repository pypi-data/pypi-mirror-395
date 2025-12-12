import sys
from setuptools import setup, find_packages

# Detect the environment (CPython vs MicroPython)
is_micropython = sys.implementation.name == "micropython"

# Conditional requirements based on the environment
install_requires = []

if not is_micropython:
    # Add dependencies for CPython
    install_requires.extend([
        "requests",  # Standard HTTP requests library
    ])
else:
    # Add dependencies for MicroPython (if needed)
    install_requires.extend([
        # "micropython-urequests",  # Optional: Uncomment if using a package manager like mip
    ])

setup(
    name="om2m-client",
    version="0.1.3",
    description="A client for interacting with OM2M CSE, compatible with CPython and MicroPython.",
    long_description=open("README.md").read() if not is_micropython else "",
    long_description_content_type="text/markdown",
    author="Ahmad Hammad, Omar Hourani",
    author_email="Ahmad.Hammad@ieee.com, Omar.Hourani@ieee.org",
    url="https://github.com/SCRCE/micropython-om2m-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
    install_requires=install_requires,
    extras_require={
        "dev": ["pytest", "flake8"],  # Optional: Add development dependencies here
    },
)
