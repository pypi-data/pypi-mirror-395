from importlib import metadata
from pathlib import Path
from setuptools import setup, find_packages

# setup.py - packaging for the cps-hhbk project

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8") if (HERE / "README.md").exists() else ""

# package name (use dash for distribution name, underscore for import name)
DIST_NAME = "cps-hhbk"
PKG_NAME = "cps_hhbk"

# attempt to derive version from installed distribution; fall back to a default
try:
    VERSION = metadata.version(DIST_NAME)
except metadata.PackageNotFoundError:
    VERSION = "0.0.1"

setup(
    name=DIST_NAME,
    version=VERSION,
    description="cps-hhbk: concise description goes here",
    long_description=README,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="",
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    install_requires=[
        "gpiozero"
    ],
    python_requires=">=3.10",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    zip_safe=False,
)