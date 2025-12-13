from setuptools import setup, find_packages
import json
import os

# Load version from version.json
ROOT = os.path.dirname(__file__)
version_json = os.path.join(ROOT, "sentior_platform", "generated", "version.py")

version_globals = {}
with open(version_json) as f:
    exec(f.read(), version_globals)

VERSION = version_globals["SDK_VERSION"]

setup(
    name="sentior-platform-sdk",
    version=VERSION,
    description="Internal Sentior Platform SDK",
    author="Sentior",
    packages=find_packages(),
)
