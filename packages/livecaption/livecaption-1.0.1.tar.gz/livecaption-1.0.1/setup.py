#!/usr/bin/env python3
"""
LiveCaption Setup Script

This script handles installation and post-install configuration
for the LiveCaption audio transcription system.
"""

import os
import sys
import subprocess
from pathlib import Path

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop


def run_post_install():
    """Run post-installation setup tasks."""
    try:
        # Import and run the installer
        from livecaption.installer import main as setup_main

        print("\n" + "=" * 60)
        print("📦 LiveCaption Installed - Running Setup")
        print("=" * 60 + "\n")

        # Run the installer automatically
        setup_main()

    except ImportError:
        # If running during initial install, the module might not be available yet
        # In that case, print instructions for manual setup
        print("\n" + "=" * 60)
        print("✅ LiveCaption installed successfully!")
        print("=" * 60)
        print("\n⚠️  IMPORTANT: You must run setup to complete installation:")
        print("\n  livecaption-setup")
        print("\nThis will:")
        print("  • Register the native messaging host for Firefox")
        print("  • Detect available audio sources")
        print("  • Configure model cache directory")
        print("  • Set up Firefox extension integration")
        print("\nAfter setup, install the Firefox extension from:")
        print("  https://addons.mozilla.org/firefox/addon/livecaption/")
        print("\nFor help:")
        print("  livecaption --help")
        print("=" * 60 + "\n")
    except (KeyboardInterrupt, EOFError):
        print("\n")
        print("=" * 60)
        print("⚠️  Setup interrupted")
        print("=" * 60)
        print("\nYou can complete setup later by running:")
        print("  livecaption-setup")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n⚠️  Setup encountered an error: {e}")
        print("\nYou can try running setup again with:")
        print("  livecaption-setup\n")


class PostInstallCommand(install):
    """Post-installation command for pip install."""
    
    def run(self):
        install.run(self)
        run_post_install()


class PostDevelopCommand(develop):
    """Post-installation command for pip install -e (development mode)."""
    
    def run(self):
        develop.run(self)
        run_post_install()


# Read long description from README
this_directory = Path(__file__).parent
long_description = ""
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")


setup(
    name="livecaption",
    version="1.0.0",
    description="Real-time audio transcription for video streaming with Firefox browser integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Boris",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.36.0",
        "accelerate>=0.25.0",
        "sounddevice>=0.4.6",
        "numpy>=1.24.0",
        "silero-vad>=5.0.0",
    ],
    extras_require={
        "faster-whisper": ["faster-whisper>=0.10.0"],
        "dev": ["pytest>=7.0.0", "black>=23.0.0", "mypy>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "livecaption=livecaption.main:main",
            "livecaption-setup=livecaption.installer:main",
            "livecaption-uninstall=livecaption.uninstaller:main",
            "livecaption-host=livecaption.native_host:main",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostDevelopCommand,
    },
    include_package_data=True,
    package_data={
        "livecaption": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Video",
    ],
)
