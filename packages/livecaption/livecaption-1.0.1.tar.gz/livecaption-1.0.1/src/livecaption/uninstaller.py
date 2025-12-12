#!/usr/bin/env python3
"""
LiveCaption Uninstaller

Removes all LiveCaption components from the system.
"""

import shutil
import subprocess
import sys
from pathlib import Path


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


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ️  {message}")


def confirm_uninstall() -> bool:
    """Ask user to confirm uninstallation."""
    print_info("This will remove:")
    print("  • Native messaging host (~/.mozilla/native-messaging-hosts/)")
    print("  • Configuration files (~/.config/livecaption/)")
    print("  • The Firefox extension will remain installed")
    print("    (remove manually from about:addons)")
    
    try:
        response = input("\nAre you sure you want to uninstall LiveCaption? (y/N): ").strip().lower()
        return response == 'y'
    except (KeyboardInterrupt, EOFError):
        print("\n")
        return False


def remove_native_messaging_host() -> bool:
    """Remove native messaging host files."""
    print_info("Removing native messaging host...")
    
    hosts_dir = Path.home() / ".mozilla" / "native-messaging-hosts"
    removed = False
    
    # Remove manifest
    manifest_path = hosts_dir / "livecaption_host.json"
    if manifest_path.exists():
        manifest_path.unlink()
        print_success(f"Removed {manifest_path}")
        removed = True
    
    # Remove wrapper script
    wrapper_path = hosts_dir / "livecaption_host.py"
    if wrapper_path.exists():
        wrapper_path.unlink()
        print_success(f"Removed {wrapper_path}")
        removed = True
    
    if not removed:
        print_warning("Native messaging host not found")
    
    return True


def remove_config() -> bool:
    """Remove configuration files."""
    print_info("Removing configuration files...")
    
    config_dir = Path.home() / ".config" / "livecaption"
    
    if config_dir.exists():
        shutil.rmtree(config_dir)
        print_success(f"Removed {config_dir}")
        return True
    else:
        print_warning("Configuration directory not found")
        return True


def remove_output_directory() -> bool:
    """Ask if user wants to remove output directory."""
    output_dir = Path.home() / "Documents" / "LiveCaption"
    
    if not output_dir.exists():
        return True
    
    print_info(f"\nOutput directory found: {output_dir}")
    
    # Check if it has files
    files = list(output_dir.glob("*.srt"))
    if files:
        print_info(f"  Contains {len(files)} subtitle file(s)")
    
    try:
        response = input("Remove output directory and subtitle files? (y/N): ").strip().lower()
        if response == 'y':
            shutil.rmtree(output_dir)
            print_success(f"Removed {output_dir}")
    except (KeyboardInterrupt, EOFError):
        print("\n")
        print_info("Output directory preserved")
    
    return True


def uninstall_pip_package() -> bool:
    """Uninstall the livecaption pip package."""
    print_info("Uninstalling Python package...")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "livecaption", "-y"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print_success("Python package uninstalled")
            return True
        else:
            print_warning("Could not uninstall Python package")
            print_info("You can manually run: pip uninstall livecaption")
            return False
    except Exception as e:
        print_warning(f"Error uninstalling package: {e}")
        print_info("You can manually run: pip uninstall livecaption")
        return False


def main():
    """Run the uninstaller."""
    print_header("LiveCaption Uninstaller")

    # Confirm uninstallation
    if not confirm_uninstall():
        print_info("Uninstallation cancelled")
        return 0

    print()

    # Remove components
    remove_native_messaging_host()
    remove_config()
    remove_output_directory()

    # Uninstall pip package
    print()
    uninstall_pip_package()

    # Print completion message
    print("\n" + "=" * 60)
    print("✅ LiveCaption Completely Uninstalled")
    print("=" * 60)

    print("\nRemaining step:")
    print("  • Remove Firefox extension (optional):")
    print("    - Open Firefox")
    print("    - Go to about:addons")
    print("    - Find LiveCaption and click 'Remove'")
    print("=" * 60 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
