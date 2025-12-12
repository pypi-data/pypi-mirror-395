#!/usr/bin/env python3
"""
LiveCaption Installer

Handles post-installation setup including:
- Native messaging host registration for Firefox
- Firefox extension installation
- Audio source detection
- Configuration initialization
"""

import configparser
import json
import logging
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger(__name__)


# Extension ID must match manifest.json
EXTENSION_ID = "boki.priv@proton.me"
NATIVE_HOST_NAME = "livecaption_host"


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"🎙️  {title}")
    print("=" * 60 + "\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✓ {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠️  {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"❌ {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ️  {message}")


def get_native_host_path() -> Path:
    """Get the path to the native_host.py script."""
    # First, try to find it in the installed package
    try:
        import livecaption
        package_dir = Path(livecaption.__file__).parent
        native_host = package_dir / "native_host.py"
        if native_host.exists():
            return native_host
    except ImportError:
        pass
    
    # Fallback to script directory
    return Path(__file__).parent / "native_host.py"


def get_extension_source_dir() -> Optional[Path]:
    """Get the path to the extension source directory."""
    # Try multiple locations
    possible_paths = [
        # Installed package
        Path(__file__).parent.parent.parent / "extension",
        # Development layout
        Path(__file__).parent.parent.parent.parent / "extension",
        # Current directory
        Path.cwd() / "extension",
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "manifest.json").exists():
            return path
    
    return None


def get_firefox_profiles_dir() -> Path:
    """Get the Firefox profiles directory."""
    return Path.home() / ".mozilla" / "firefox"


def get_firefox_profiles() -> List[Tuple[str, Path]]:
    """
    Get list of Firefox profiles.
    
    Returns:
        List of (profile_name, profile_path) tuples
    """
    profiles_dir = get_firefox_profiles_dir()
    profiles_ini = profiles_dir / "profiles.ini"
    
    if not profiles_ini.exists():
        return []
    
    config = configparser.ConfigParser()
    config.read(profiles_ini)
    
    profiles = []
    for section in config.sections():
        if section.startswith("Profile"):
            name = config.get(section, "Name", fallback="Unknown")
            path = config.get(section, "Path", fallback=None)
            is_relative = config.getboolean(section, "IsRelative", fallback=True)
            is_default = config.getboolean(section, "Default", fallback=False)
            
            if path:
                if is_relative:
                    profile_path = profiles_dir / path
                else:
                    profile_path = Path(path)
                
                if profile_path.exists():
                    profiles.append((name, profile_path, is_default))
    
    return profiles


def get_default_firefox_profile() -> Optional[Path]:
    """Get the default Firefox profile path."""
    profiles = get_firefox_profiles()
    
    # Look for default profile
    for name, path, is_default in profiles:
        if is_default:
            return path
    
    # Look for default-release profile
    for name, path, _ in profiles:
        if "default-release" in str(path) or "default-release" in name.lower():
            return path
    
    # Return first profile if any exist
    if profiles:
        return profiles[0][1]
    
    return None


def register_native_messaging_host() -> bool:
    """
    Register the native messaging host with Firefox.
    
    Creates the manifest file in ~/.mozilla/native-messaging-hosts/
    """
    print_info("Registering native messaging host...")
    
    # Create native messaging hosts directory
    hosts_dir = Path.home() / ".mozilla" / "native-messaging-hosts"
    hosts_dir.mkdir(parents=True, exist_ok=True)
    
    # Get path to native_host.py
    native_host_path = get_native_host_path()
    
    if not native_host_path.exists():
        print_error(f"Native host script not found at {native_host_path}")
        return False
    
    # Make native host executable
    native_host_path.chmod(native_host_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    # Create wrapper script that uses the correct Python interpreter
    wrapper_path = hosts_dir / "livecaption_host.py"
    # Add parent of livecaption package to path (e.g., /path/to/src)
    package_parent = native_host_path.parent.parent
    wrapper_content = f'''#!/usr/bin/env python3
"""LiveCaption Native Messaging Host Wrapper"""
import sys
import os

# Add the parent directory of livecaption package to Python path
livecaption_dir = "{package_parent}"
if livecaption_dir not in sys.path:
    sys.path.insert(0, livecaption_dir)

# Now import and run the native host
from livecaption.native_host import main

if __name__ == "__main__":
    main()
'''
    
    with open(wrapper_path, "w") as f:
        f.write(wrapper_content)
    wrapper_path.chmod(wrapper_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
    # Create native messaging manifest
    manifest = {
        "name": NATIVE_HOST_NAME,
        "description": "LiveCaption Native Messaging Host - Real-time audio transcription",
        "path": str(wrapper_path),
        "type": "stdio",
        "allowed_extensions": [EXTENSION_ID],
    }
    
    manifest_path = hosts_dir / f"{NATIVE_HOST_NAME}.json"
    
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print_success(f"Native messaging host registered at {manifest_path}")
    return True


def install_firefox_extension() -> bool:
    """
    Provide instructions to install the Firefox extension from the store.
    """
    print_info("Firefox Extension Installation...")

    print_info("\n" + "=" * 60)
    print_info("📦 INSTALL LIVECAPTION EXTENSION")
    print_info("=" * 60)

    print_info("\nThe LiveCaption extension is available on Firefox Add-ons:")
    print_info("  🔗 https://addons.mozilla.org/firefox/addon/livecaption/")

    print_info("\n" + "=" * 60)

    # Prompt to open the page
    try:
        open_browser = input("\nOpen Firefox Add-ons page now? (Y/n): ").strip().lower()

        if open_browser != 'n':
            print_info("\nOpening Firefox Add-ons page...")
            try:
                subprocess.run(
                    ["firefox", "https://addons.mozilla.org/firefox/addon/livecaption/"],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print_success("✓ Firefox opened")
            except Exception as e:
                print_warning(f"Could not open Firefox automatically: {e}")
                print_info("Please visit: https://addons.mozilla.org/firefox/addon/livecaption/")

        print_info("\n" + "=" * 60)
        print_info("After installing the extension:")
        print_info("  1. Click 'Add to Firefox'")
        print_info("  2. Confirm the installation")
        print_info("  3. The LiveCaption icon will appear in your toolbar")
        print_info("  4. Click it to start using LiveCaption!")
        print_info("=" * 60)

    except (KeyboardInterrupt, EOFError):
        print("\n")
        print_info("You can install the extension later from:")
        print_info("  https://addons.mozilla.org/firefox/addon/livecaption/")

    return True


def detect_audio_sources() -> List[dict]:
    """
    Detect available audio sources.
    
    Returns:
        List of audio source dictionaries
    """
    print_info("Detecting audio sources...")
    
    sources = []
    
    try:
        result = subprocess.run(
            ["pactl", "list", "sources", "short"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                name = parts[1]
                if "monitor" in name.lower():
                    sources.append({
                        "name": name,
                        "type": "monitor",
                    })
                    
    except subprocess.TimeoutExpired:
        print_warning("Timeout detecting audio sources")
    except FileNotFoundError:
        print_warning("pactl not found - PulseAudio/PipeWire may not be installed")
    except Exception as e:
        print_warning(f"Error detecting audio sources: {e}")
    
    return sources


def initialize_config() -> bool:
    """Initialize default configuration."""
    print_info("Initializing configuration...")

    try:
        from livecaption.config import get_config, save_config, Config

        # Load existing config or create new
        config = get_config()

        # Detect and set default audio source
        sources = detect_audio_sources()
        if sources:
            config.default_audio_source = sources[0]["name"]

        # Ensure output directory exists
        config.ensure_output_dir()

        # Prompt for model cache directory
        print_info("\n" + "=" * 60)
        print_info("MODEL CACHE CONFIGURATION")
        print_info("=" * 60)
        print_info("\nAI models will be downloaded on first use (~1-6GB each).")
        print_info("First download can take 5-30 minutes depending on connection.")

        if config.model_cache_dir:
            print_info(f"\nCurrent cache directory: {config.model_cache_dir}")
            change = input("Change cache directory? (y/N): ").strip().lower()
            if change != 'y':
                cache_path = config.model_cache_dir
            else:
                cache_path = None
        else:
            cache_path = None

        if cache_path is None:
            print_info("\nDefault: ~/.cache/huggingface (~/.cache/torch for some models)")
            custom = input("Set custom cache directory? (y/N): ").strip().lower()

            if custom == 'y':
                while True:
                    cache_input = input("Enter cache directory path: ").strip()
                    if cache_input:
                        cache_dir = Path(cache_input).expanduser().resolve()
                        try:
                            cache_dir.mkdir(parents=True, exist_ok=True)
                            config.model_cache_dir = str(cache_dir)
                            print_success(f"✓ Cache directory set to: {cache_dir}")

                            # Set environment variable for this session
                            import os
                            os.environ['TRANSFORMERS_CACHE'] = str(cache_dir)
                            os.environ['HF_HOME'] = str(cache_dir)

                            print_info("\n💡 To make this permanent, add to ~/.bashrc:")
                            print_info(f"   export TRANSFORMERS_CACHE='{cache_dir}'")
                            print_info(f"   export HF_HOME='{cache_dir}'")
                            break
                        except Exception as e:
                            print_warning(f"Could not create directory: {e}")
                            retry = input("Try again? (y/N): ").strip().lower()
                            if retry != 'y':
                                break
                    else:
                        break
            else:
                print_info("✓ Using default cache location")

        # Save configuration
        if save_config(config):
            print_success(f"✓ Configuration saved to ~/.config/livecaption/config.json")
            return True
        else:
            print_warning("Could not save configuration")
            return False

    except (KeyboardInterrupt, EOFError):
        print("\n")
        print_warning("Configuration setup cancelled")
        return False
    except Exception as e:
        print_warning(f"Could not initialize configuration: {e}")
        return False


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    print_info("Checking dependencies...")
    
    missing = []
    
    # Check Python packages
    packages = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("sounddevice", "SoundDevice"),
        ("numpy", "NumPy"),
    ]
    
    for module, name in packages:
        try:
            __import__(module)
        except ImportError:
            missing.append(name)
    
    # Check system commands
    commands = [
        ("pactl", "PulseAudio utilities (pulseaudio-utils)"),
    ]
    
    for cmd, name in commands:
        if shutil.which(cmd) is None:
            missing.append(name)
    
    if missing:
        print_warning(f"Missing dependencies: {', '.join(missing)}")
        return False
    
    print_success("All dependencies found")
    return True


def setup_native_messaging():
    """Main setup function (entry point for livecaption-setup command)."""
    main()


def main():
    """Run the installer."""
    print_header("LiveCaption Setup")
    
    success = True
    
    # Check dependencies
    check_dependencies()
    
    # Register native messaging host
    if not register_native_messaging_host():
        success = False
    
    # Install Firefox extension
    if not install_firefox_extension():
        # Not critical - can be installed manually
        pass
    
    # Detect audio sources
    sources = detect_audio_sources()
    if sources:
        print_success(f"Found {len(sources)} audio source(s):")
        for i, source in enumerate(sources, 1):
            print(f"   {i}. {source['name']}")
    else:
        print_warning("No monitor audio sources found")
        print_info("Make sure you have audio playing to detect sources")
    
    # Initialize configuration
    initialize_config()
    
    # Print completion message
    print("\n" + "=" * 60)
    if success:
        print("✅ Installation Complete!")
    else:
        print("⚠️  Installation completed with warnings")
    print("=" * 60)
    
    print("\nNext steps:")
    print("  1. Restart Firefox")
    print("  2. The LiveCaption extension should appear in your toolbar")
    print("  3. If not, go to about:debugging → This Firefox → Load Temporary Add-on")
    print(f"     and select the manifest.json in the extension folder")
    print("  4. Click the extension icon and start recording!")
    
    print("\nUsage:")
    print("  • Click the LiveCaption icon in Firefox toolbar")
    print("  • Select your audio source and model")
    print("  • Click 'Start Recording'")
    print("  • Play a video - transcription will appear in the popup")
    
    print("\nCommand line usage:")
    print("  livecaption --model anime-whisper --output output.srt")
    
    print("\nFor help:")
    print("  livecaption --help")
    print("=" * 60 + "\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
