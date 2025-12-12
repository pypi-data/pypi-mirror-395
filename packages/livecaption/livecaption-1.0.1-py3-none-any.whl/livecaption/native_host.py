#!/usr/bin/env python3
"""
LiveCaption Native Messaging Host

This script acts as a bridge between the Firefox extension and the
LiveCaption transcription engine. It implements the Firefox Native
Messaging protocol for bi-directional communication.

Protocol:
- Messages are JSON with a 4-byte length prefix (native byte order)
- stdin: receives commands from Firefox
- stdout: sends responses/transcriptions to Firefox
"""

import json
import logging
import os
import signal
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging to stderr (stdout is reserved for native messaging)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


class NativeMessagingHost:
    """
    Native Messaging Host for Firefox extension communication.
    
    Handles the native messaging protocol and manages the transcription
    subprocess lifecycle.
    """
    
    def __init__(self):
        self.transcription_process: Optional[subprocess.Popen] = None
        self.output_thread: Optional[threading.Thread] = None
        self.is_running = True
        self.is_recording = False
        self.current_output_file: Optional[str] = None
        
        # Find the livecaption module path
        self.module_path = self._find_module_path()
        
        # Set up signal handlers for clean shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _find_module_path(self) -> Path:
        """Find the path to the livecaption main module."""
        # Try to find it in the package
        try:
            import livecaption
            return Path(livecaption.__file__).parent / "main.py"
        except ImportError:
            pass
        
        # Fallback to current directory
        return Path(__file__).parent / "main.py"
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
    
    def read_message(self) -> Optional[Dict[str, Any]]:
        """
        Read a message from stdin using native messaging protocol.
        
        Returns:
            Parsed JSON message or None if no more messages
        """
        try:
            # Read 4-byte length prefix
            raw_length = sys.stdin.buffer.read(4)
            if not raw_length or len(raw_length) < 4:
                return None
            
            # Unpack length (native byte order)
            message_length = struct.unpack("@I", raw_length)[0]
            
            if message_length == 0:
                return None
            
            if message_length > 1024 * 1024:  # 1MB limit
                logger.error(f"Message too large: {message_length} bytes")
                return None
            
            # Read message content
            message_data = sys.stdin.buffer.read(message_length)
            if len(message_data) < message_length:
                logger.error("Incomplete message received")
                return None
            
            # Parse JSON
            message = json.loads(message_data.decode("utf-8"))
            logger.debug(f"Received message: {message}")
            return message
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in message: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading message: {e}")
            return None
    
    def send_message(self, message: Dict[str, Any]) -> None:
        """
        Send a message to the browser using native messaging protocol.
        
        Args:
            message: Dictionary to send as JSON
        """
        try:
            # Encode message as JSON
            encoded = json.dumps(message, ensure_ascii=False).encode("utf-8")
            
            # Write length prefix (native byte order)
            sys.stdout.buffer.write(struct.pack("@I", len(encoded)))
            
            # Write message content
            sys.stdout.buffer.write(encoded)
            sys.stdout.buffer.flush()
            
            logger.debug(f"Sent message: {message.get('type', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    def send_response(self, success: bool, data: Optional[Dict] = None, error: Optional[str] = None) -> None:
        """Send a standard response message."""
        message = {
            "type": "response",
            "success": success,
            "timestamp": time.time(),
        }
        if data:
            message["data"] = data
        if error:
            message["error"] = error
        self.send_message(message)
    
    def send_transcription(self, text: str, start_time: float, end_time: float) -> None:
        """Send a transcription update to the browser."""
        self.send_message({
            "type": "transcription",
            "text": text,
            "start": start_time,
            "end": end_time,
            "timestamp": time.time(),
        })
    
    def send_status(self, status: str, details: Optional[Dict] = None) -> None:
        """Send a status update to the browser."""
        message = {
            "type": "status",
            "status": status,
            "timestamp": time.time(),
        }
        if details:
            message["details"] = details
        self.send_message(message)
    
    def handle_start(self, config: Dict[str, Any]) -> None:
        """
        Handle START command - launch transcription process.
        
        Args:
            config: Configuration dictionary with model, output, etc.
        """
        if self.is_recording:
            self.send_response(False, error="Already recording")
            return
        
        try:
            # Build command arguments
            model = config.get("model", "kotoba-v1.0")
            output = config.get("output", f"livecaption_{int(time.time())}.srt")
            device = config.get("device", "auto")
            chunk_duration = config.get("chunk_duration", 30.0)
            
            # Expand output path
            output_path = Path(output).expanduser()
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Only add timestamp if file already exists
            if output_path.exists():
                stem = output_path.stem
                suffix = output_path.suffix
                timestamp = time.strftime("%Y-%m-%dT%H-%M-%S")
                output_path = output_path.parent / f"{stem}_{timestamp}{suffix}"
                logger.info(f"File exists, using timestamped name: {output_path.name}")

            self.current_output_file = str(output_path)
            
            # Build command
            cmd = [
                sys.executable,
                str(self.module_path),
                "--model", model,
                "--output", self.current_output_file,
                "--device", device,
                "--chunk-duration", str(chunk_duration),
                "--skip-audio-setup",  # We handle audio source externally
            ]
            
            # Set audio source if specified, otherwise try auto-detect browser audio
            env = os.environ.copy()
            audio_source = config.get("audio_source")

            if not audio_source:
                # Try to auto-detect browser audio
                from livecaption.config import get_browser_audio_source
                audio_source = get_browser_audio_source()
                if audio_source:
                    logger.info(f"Auto-detected browser audio source: {audio_source}")

            if audio_source:
                # Set PulseAudio default source (sounddevice/PortAudio doesn't respect PULSE_SOURCE env var)
                try:
                    subprocess.run(
                        ["pactl", "set-default-source", audio_source],
                        check=True,
                        timeout=5
                    )
                    logger.info(f"Set default audio source to: {audio_source}")
                except Exception as e:
                    logger.warning(f"Could not set default audio source: {e}")
                    # Still set env var as fallback
                    env["PULSE_SOURCE"] = audio_source
            else:
                logger.info("No audio source specified, using system default")

            # Force unbuffered output for real-time transcription
            env["PYTHONUNBUFFERED"] = "1"

            logger.info(f"Starting transcription: {' '.join(cmd)}")

            # Launch process
            self.transcription_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                text=True,
                bufsize=1,  # Line buffered
            )
            
            self.is_recording = True
            
            # Start output reader thread
            self.output_thread = threading.Thread(
                target=self._read_process_output,
                daemon=True
            )
            self.output_thread.start()
            
            self.send_response(True, data={
                "message": "Recording started",
                "output_file": self.current_output_file,
                "model": model,
            })
            self.send_status("recording")
            
        except Exception as e:
            logger.error(f"Failed to start transcription: {e}")
            self.send_response(False, error=str(e))
    
    def handle_stop(self) -> None:
        """Handle STOP command - terminate transcription process."""
        if not self.is_recording:
            self.send_response(False, error="Not recording")
            return
        
        try:
            self._stop_transcription()
            self.send_response(True, data={
                "message": "Recording stopped",
                "output_file": self.current_output_file,
            })
            self.send_status("idle")
            
        except Exception as e:
            logger.error(f"Error stopping transcription: {e}")
            self.send_response(False, error=str(e))
    
    def _stop_transcription(self) -> None:
        """Stop the transcription process."""
        if self.transcription_process:
            # Send SIGINT for graceful shutdown (allows processing remaining audio)
            self.transcription_process.send_signal(signal.SIGINT)
            
            # Wait for process to finish (with timeout)
            try:
                self.transcription_process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                logger.warning("Transcription process didn't stop gracefully, killing...")
                self.transcription_process.kill()
                self.transcription_process.wait()
            
            self.transcription_process = None
        
        self.is_recording = False
    
    def _read_process_output(self) -> None:
        """Read and forward transcription process output."""
        if not self.transcription_process or not self.transcription_process.stdout:
            return
        
        try:
            for line in self.transcription_process.stdout:
                line = line.strip()
                if not line:
                    continue
                
                # Parse transcription output lines
                # Format: [MM:SS --> MM:SS] Text or   [MM:SS --> MM:SS] Text (with leading spaces)
                if "[" in line and "-->" in line and "]" in line:
                    try:
                        # Extract timestamp and text
                        bracket_start = line.index("[")
                        bracket_end = line.index("]")
                        timestamp_part = line[bracket_start + 1:bracket_end]
                        text = line[bracket_end + 1:].strip()
                        
                        start_str, end_str = timestamp_part.split("-->")
                        start_time = self._parse_timestamp(start_str.strip())
                        end_time = self._parse_timestamp(end_str.strip())
                        
                        if text:
                            self.send_transcription(text, start_time, end_time)
                    except Exception as e:
                        logger.debug(f"Could not parse transcription line: {line}")
                else:
                    # Send as log message
                    self.send_message({
                        "type": "log",
                        "message": line,
                        "timestamp": time.time(),
                    })
                    
        except Exception as e:
            logger.error(f"Error reading process output: {e}")
        
        # Process ended
        if self.is_recording:
            self.is_recording = False
            self.send_status("idle", {"reason": "process_ended"})
    
    def _parse_timestamp(self, ts: str) -> float:
        """Parse timestamp string (MM:SS or HH:MM:SS,mmm) to seconds."""
        try:
            # Handle SRT format (HH:MM:SS,mmm)
            if "," in ts:
                time_part, ms = ts.split(",")
                parts = time_part.split(":")
                if len(parts) == 3:
                    h, m, s = map(int, parts)
                    return h * 3600 + m * 60 + s + int(ms) / 1000
            
            # Handle simple format (MM:SS)
            parts = ts.split(":")
            if len(parts) == 2:
                m, s = map(int, parts)
                return m * 60 + s
            elif len(parts) == 3:
                h, m, s = map(int, parts)
                return h * 3600 + m * 60 + s
                
        except Exception:
            pass
        return 0.0
    
    def handle_get_sources(self) -> None:
        """Handle GET_SOURCES command - list available audio sources."""
        try:
            from livecaption.config import get_audio_sources
            sources = get_audio_sources()
            self.send_response(True, data={"sources": sources})
        except Exception as e:
            logger.error(f"Error getting audio sources: {e}")
            self.send_response(False, error=str(e))
    
    def handle_get_config(self) -> None:
        """Handle GET_CONFIG command - return current configuration."""
        try:
            from livecaption.config import get_config
            config = get_config()
            self.send_response(True, data={"config": config.to_dict()})
        except Exception as e:
            logger.error(f"Error getting config: {e}")
            self.send_response(False, error=str(e))
    
    def handle_save_config(self, config_data: Dict[str, Any]) -> None:
        """Handle SAVE_CONFIG command - save configuration."""
        try:
            from livecaption.config import Config, save_config
            config = Config.from_dict(config_data)
            if save_config(config):
                self.send_response(True, data={"message": "Configuration saved"})
            else:
                self.send_response(False, error="Failed to save configuration")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            self.send_response(False, error=str(e))
    
    def handle_ping(self) -> None:
        """Handle PING command - health check."""
        self.send_response(True, data={
            "message": "pong",
            "is_recording": self.is_recording,
            "version": "1.0.0",
        })
    
    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Route incoming message to appropriate handler.
        
        Args:
            message: Parsed message dictionary
        """
        action = message.get("action", "").upper()
        
        handlers = {
            "START": lambda: self.handle_start(message.get("config", {})),
            "STOP": self.handle_stop,
            "GET_SOURCES": self.handle_get_sources,
            "GET_CONFIG": self.handle_get_config,
            "SAVE_CONFIG": lambda: self.handle_save_config(message.get("config", {})),
            "PING": self.handle_ping,
        }
        
        handler = handlers.get(action)
        if handler:
            handler()
        else:
            logger.warning(f"Unknown action: {action}")
            self.send_response(False, error=f"Unknown action: {action}")
    
    def run(self) -> None:
        """Main message loop."""
        logger.info("Native messaging host started")
        self.send_status("ready")
        
        try:
            while self.is_running:
                message = self.read_message()
                if message is None:
                    # EOF or error - browser disconnected
                    logger.info("No more messages, shutting down")
                    break
                
                self.handle_message(message)
                
        except Exception as e:
            logger.error(f"Error in message loop: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self) -> None:
        """Clean up and shut down."""
        logger.info("Shutting down native messaging host")
        self.is_running = False
        
        if self.is_recording:
            self._stop_transcription()
        
        logger.info("Shutdown complete")


def main():
    """Entry point for native messaging host."""
    host = NativeMessagingHost()
    host.run()


if __name__ == "__main__":
    main()
