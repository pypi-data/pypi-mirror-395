#!/usr/bin/env python3
"""
Color Notify - Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path
import traceback

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

def get_version():
    """Get version from __version__.py file"""
    try:
        version_file = Path(__file__).parent / "__version__.py"
        if not version_file.is_file():
            return "2.0.1"
        if version_file.is_file():
            with open(version_file, "r") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        parts = line.split("=")
                        if len(parts) == 2:
                            return parts[1].strip().strip('"').strip("'")
    except Exception as e:
        if os.getenv('TRACEBACK') and os.getenv('TRACEBACK') in ['1', 'true', 'True']:
            print(traceback.format_exc())
        else:
            print(f"ERROR: {e}")
    return "2.0.1"

setup(
    name="color-notify",
    version=get_version(),
    author="Hadi Cahyadi",
    author_email="cumulus13@gmail.com",
    description="Desktop notification tool for clipboard color code detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cumulus13/color-notify",
    project_urls={
        "Bug Tracker": "https://github.com/cumulus13/color-notify/issues",
        "Documentation": "https://github.com/cumulus13/color-notify#readme",
        "Source Code": "https://github.com/cumulus13/color-notify",
    },
    packages=find_packages(),
    py_modules=["color_notify"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Topic :: Software Development :: User Interfaces",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: X11 Applications :: Qt",
    ],
    keywords=[
        "color", "notification", "clipboard", "monitor", "desktop",
        "growl", "hex", "rgb", "color-picker", "system-tray",
        "pyqt5", "qt", "gui"
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyQt5>=5.15.0",
        "version_get",
        "pynput>=1.7.6",
    ],
    entry_points={
        "console_scripts": [
            "color-notify=color_notify:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ini", "*.md", "LICENSE"],
    },
    zip_safe=False,
    license="MIT",
    license_files=["LICENSE"]
)
