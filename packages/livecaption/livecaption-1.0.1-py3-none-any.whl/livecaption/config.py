#!/usr/bin/env python3
"""
LiveCaption Configuration Management

Handles reading, writing, and validating configuration settings.
Settings are stored in ~/.config/livecaption/config.json
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


# Default configuration values
DEFAULT_CONFIG = {
    "language": "ja",
    "model": "kotoba-v1.0",
    "device": "auto",
    "output_dir": "~/Documents/LiveCaption",
    "auto_sync": True,
    "default_audio_source": None,
    "chunk_duration": 30.0,
    "auto_start_on_video": True,
    "show_notifications": True,
    "dark_mode": "system",
    "model_cache_dir": None,  # None means use default (~/.cache/huggingface)
}

# Valid values for configuration options
VALID_LANGUAGES = ["ja", "en", "ko", "zh", "auto"]
VALID_MODELS = ["kotoba-v1.0", "kotoba-v2.0", "anime-whisper", "large-v3", "medium"]
VALID_DEVICES = ["auto", "cuda", "cpu"]
VALID_DARK_MODES = ["system", "light", "dark"]


@dataclass
class Config:
    """Configuration settings for LiveCaption."""

    language: str = "ja"
    model: str = "kotoba-v1.0"
    device: str = "auto"
    output_dir: str = "~/Documents/LiveCaption"
    auto_sync: bool = True
    default_audio_source: Optional[str] = None
    chunk_duration: float = 30.0
    auto_start_on_video: bool = True
    show_notifications: bool = True
    dark_mode: str = "system"
    model_cache_dir: Optional[str] = None
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        self.validate()
    
    def validate(self) -> None:
        """Validate configuration values."""
        errors: List[str] = []
        
        if self.language not in VALID_LANGUAGES:
            errors.append(f"Invalid language '{self.language}'. Must be one of: {VALID_LANGUAGES}")
        
        if self.model not in VALID_MODELS:
            errors.append(f"Invalid model '{self.model}'. Must be one of: {VALID_MODELS}")
        
        if self.device not in VALID_DEVICES:
            errors.append(f"Invalid device '{self.device}'. Must be one of: {VALID_DEVICES}")
        
        if self.dark_mode not in VALID_DARK_MODES:
            errors.append(f"Invalid dark_mode '{self.dark_mode}'. Must be one of: {VALID_DARK_MODES}")
        
        if not isinstance(self.chunk_duration, (int, float)) or self.chunk_duration <= 0:
            errors.append(f"Invalid chunk_duration '{self.chunk_duration}'. Must be positive number")
        
        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create configuration from dictionary."""
        # Filter out unknown keys
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)
    
    def get_output_dir(self) -> Path:
        """Get the output directory as a resolved Path."""
        return Path(self.output_dir).expanduser().resolve()
    
    def ensure_output_dir(self) -> Path:
        """Ensure output directory exists and return its path."""
        output_path = self.get_output_dir()
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path


def get_config_dir() -> Path:
    """Get the configuration directory path."""
    config_dir = Path.home() / ".config" / "livecaption"
    return config_dir


def get_config_file() -> Path:
    """Get the configuration file path."""
    return get_config_dir() / "config.json"


def get_config() -> Config:
    """
    Load configuration from file.
    
    Returns default configuration if file doesn't exist or is invalid.
    """
    config_file = get_config_file()
    
    if not config_file.exists():
        logger.info(f"Config file not found at {config_file}, using defaults")
        return Config()
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Merge with defaults for any missing keys
        merged_data = {**DEFAULT_CONFIG, **data}
        config = Config.from_dict(merged_data)
        logger.info(f"Loaded configuration from {config_file}")
        return config
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        return Config()
    except ValueError as e:
        logger.error(f"Invalid configuration values: {e}")
        return Config()
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return Config()


def save_config(config: Config) -> bool:
    """
    Save configuration to file.
    
    Args:
        config: Configuration object to save
        
    Returns:
        True if successful, False otherwise
    """
    config_file = get_config_file()
    
    try:
        # Validate before saving
        config.validate()
        
        # Ensure config directory exists
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write configuration
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved configuration to {config_file}")
        return True
        
    except ValueError as e:
        logger.error(f"Cannot save invalid configuration: {e}")
        return False
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False


def update_config(**kwargs) -> Config:
    """
    Update configuration with new values.
    
    Args:
        **kwargs: Configuration values to update
        
    Returns:
        Updated configuration object
    """
    config = get_config()
    
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            logger.warning(f"Unknown configuration key: {key}")
    
    config.validate()
    save_config(config)
    return config


def reset_config() -> Config:
    """
    Reset configuration to defaults.
    
    Returns:
        Default configuration object
    """
    config = Config()
    save_config(config)
    return config


def get_browser_audio_source() -> Optional[str]:
    """
    Attempt to automatically detect browser audio output.

    Checks if Firefox, Chrome, or other browsers are currently playing audio
    and returns the appropriate monitor source for that output.

    Returns:
        Source name if browser audio detected, None otherwise
    """
    import subprocess

    try:
        # Get sink inputs (applications playing audio)
        result = subprocess.run(
            ["pactl", "list", "sink-inputs"],
            capture_output=True,
            text=True,
            timeout=5
        )

        browser_apps = ["firefox", "chrome", "chromium", "brave", "opera", "edge"]
        current_sink_input = {}

        for line in result.stdout.split("\n"):
            stripped = line.strip()

            if stripped.startswith("Sink Input #"):
                # Check previous sink input for browser
                if (current_sink_input.get("binary") in browser_apps and
                    current_sink_input.get("sink_id")):
                    # Get sink name from ID
                    sink_name = _get_sink_name_by_id(current_sink_input["sink_id"])
                    if sink_name:
                        monitor_source = f"{sink_name}.monitor"
                        logger.info(f"Auto-detected browser audio on: {monitor_source}")
                        return monitor_source
                current_sink_input = {}

            # Parse "Sink: 51" (at top level, not in properties)
            elif stripped.startswith("Sink:") and not "=" in stripped:
                sink_id = stripped.split(":", 1)[1].strip()
                current_sink_input["sink_id"] = sink_id

            # Parse properties section
            elif "application.process.binary" in stripped and "=" in stripped:
                binary = stripped.split("=", 1)[1].strip().strip('"').lower()
                current_sink_input["binary"] = binary

        # Check last sink input
        if (current_sink_input.get("binary") in browser_apps and
            current_sink_input.get("sink_id")):
            sink_name = _get_sink_name_by_id(current_sink_input["sink_id"])
            if sink_name:
                monitor_source = f"{sink_name}.monitor"
                logger.info(f"Auto-detected browser audio on: {monitor_source}")
                return monitor_source

    except subprocess.TimeoutExpired:
        logger.error("Timeout detecting browser audio")
    except FileNotFoundError:
        logger.error("pactl not found")
    except Exception as e:
        logger.error(f"Error detecting browser audio: {e}")

    return None


def _get_sink_name_by_id(sink_id: str) -> Optional[str]:
    """Get sink name from sink ID."""
    import subprocess

    try:
        result = subprocess.run(
            ["pactl", "list", "sinks", "short"],
            capture_output=True,
            text=True,
            timeout=5
        )

        for line in result.stdout.split("\n"):
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0] == sink_id:
                return parts[1]  # Sink name

    except Exception as e:
        logger.error(f"Error getting sink name: {e}")

    return None


def get_audio_sources() -> List[Dict[str, str]]:
    """
    Get available audio sources from PulseAudio/PipeWire with detailed descriptions.

    Returns:
        List of audio source dictionaries with 'name' and 'description' keys
    """
    import subprocess

    sources = []

    try:
        # Get full source information with descriptions
        result = subprocess.run(
            ["pactl", "list", "sources"],
            capture_output=True,
            text=True,
            timeout=5
        )

        current_source = {}
        for line in result.stdout.split("\n"):
            line = line.strip()

            # New source entry starts with "Source #"
            if line.startswith("Source #"):
                # Save previous source if it was a monitor
                if current_source.get("name") and current_source.get("is_monitor"):
                    sources.append({
                        "name": current_source["name"],
                        "description": current_source.get("description", current_source["name"]),
                        "is_monitor": True,
                    })
                current_source = {}

            # Parse source name
            elif line.startswith("Name:"):
                name = line.split("Name:", 1)[1].strip()
                current_source["name"] = name
                # Check if it's a monitor source (captures system audio output)
                current_source["is_monitor"] = ".monitor" in name.lower()

            # Parse human-readable description
            elif line.startswith("Description:"):
                description = line.split("Description:", 1)[1].strip()
                current_source["description"] = description

        # Don't forget the last source
        if current_source.get("name") and current_source.get("is_monitor"):
            sources.append({
                "name": current_source["name"],
                "description": current_source.get("description", current_source["name"]),
                "is_monitor": True,
            })

    except subprocess.TimeoutExpired:
        logger.error("Timeout getting audio sources")
    except FileNotFoundError:
        logger.error("pactl not found - is PulseAudio/PipeWire installed?")
    except Exception as e:
        logger.error(f"Error getting audio sources: {e}")

    return sources


if __name__ == "__main__":
    # Test configuration
    logging.basicConfig(level=logging.DEBUG)
    
    print("Testing configuration...")
    
    # Load/create config
    config = get_config()
    print(f"Current config: {config.to_dict()}")
    
    # Get audio sources
    sources = get_audio_sources()
    print(f"Available audio sources: {sources}")
    
    # Save config
    if save_config(config):
        print(f"Config saved to {get_config_file()}")
