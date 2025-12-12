#!/usr/bin/env python3
"""
Japanese Real-Time Audio Subtitle Generator
Optimized for Japanese anime/streaming content with automatic audio routing
Supports: Kotoba-Whisper v1.0, v2.0, and Anime-Whisper
"""

import argparse
import queue
import threading
import time
import subprocess
import os
from datetime import timedelta
from pathlib import Path
from typing import Optional, List, Tuple
import numpy as np
import sounddevice as sd
import torch

# Lazy imports to speed up startup
_WhisperModel = None
_hf_pipeline = None


def lazy_import_faster_whisper():
    """Lazy import faster-whisper"""
    global _WhisperModel
    if _WhisperModel is None:
        from faster_whisper import WhisperModel
        _WhisperModel = WhisperModel
    return _WhisperModel


def lazy_import_transformers():
    """Lazy import transformers"""
    global _hf_pipeline
    if _hf_pipeline is None:
        try:
            from transformers import pipeline
            _hf_pipeline = pipeline
        except ImportError:
            raise RuntimeError(
                "Transformers not installed. Install with: pip install transformers accelerate"
            )
    return _hf_pipeline


def lazy_import_silero_vad():
    """Lazy import Silero VAD - returns (model, get_speech_timestamps_func) or (None, None)"""
    try:
        # Try the new silero-vad package first (pip install silero-vad)
        from silero_vad import load_silero_vad, get_speech_timestamps
        model = load_silero_vad()
        return model, get_speech_timestamps
    except ImportError:
        pass
    
    try:
        # Fall back to torch.hub method
        import torch
        model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False,
            trust_repo=True
        )
        # torch.hub returns (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks)
        get_speech_timestamps = utils[0]
        return model, get_speech_timestamps
    except Exception as e:
        print(f"    VAD import error: {e}")
        pass
    
    return None, None


class AudioCaptureError(Exception):
    """Custom exception for audio capture errors"""
    pass


class SubtitleSegment:
    """Represents a single subtitle segment with proper SRT formatting"""
    
    def __init__(self, index: int, start: float, end: float, text: str):
        self.index = index
        self.start = start
        self.end = end
        self.text = text.strip()
    
    def to_srt(self) -> str:
        """Convert to properly formatted SRT"""
        start_time = self._format_timestamp(self.start)
        end_time = self._format_timestamp(self.end)
        # CRITICAL: Proper SRT format with newlines
        return f"{self.index}\n{start_time} --> {end_time}\n{self.text}\n\n"
    
    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Format timestamp as HH:MM:SS,mmm"""
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


class PulseAudioManager:
    """Manages PulseAudio/PipeWire audio source configuration"""
    
    @staticmethod
    def find_monitor_sources() -> List[Tuple[str, str]]:
        """Find all monitor sources (system audio capture)"""
        try:
            result = subprocess.run(
                ['pactl', 'list', 'sources', 'short'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            monitors = []
            for line in result.stdout.strip().split('\n'):
                if 'monitor' in line.lower():
                    parts = line.split()
                    if len(parts) >= 2:
                        source_name = parts[1]
                        monitors.append((source_name, line))
            
            return monitors
        except Exception as e:
            print(f"⚠️  Could not query PulseAudio sources: {e}")
            return []
    
    @staticmethod
    def get_default_sink() -> Optional[str]:
        """Get the default audio sink"""
        try:
            result = subprocess.run(
                ['pactl', 'get-default-sink'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except Exception:
            return None
    
    @staticmethod
    def set_default_source(source_name: str) -> bool:
        """Set the default audio source"""
        try:
            result = subprocess.run(
                ['pactl', 'set-default-source', source_name],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @classmethod
    def auto_configure_audio(cls) -> bool:
        """Automatically configure audio to capture system output"""
        print("\n🔧 Auto-configuring audio source...")
        
        # First, try PULSE_SOURCE environment variable
        pulse_source = os.environ.get('PULSE_SOURCE')
        if pulse_source:
            print(f"✓ Using PULSE_SOURCE: {pulse_source}")
            return True
        
        # Find monitor sources
        monitors = cls.find_monitor_sources()
        
        if not monitors:
            print("❌ No monitor sources found!")
            print("\nManual setup required:")
            print("  pactl list sources | grep -i monitor")
            print("  export PULSE_SOURCE='your_monitor_source'")
            return False
        
        # Try to find the best monitor source
        default_sink = cls.get_default_sink()
        
        # Look for monitor of default sink
        best_monitor = None
        if default_sink:
            for source_name, _ in monitors:
                if default_sink in source_name:
                    best_monitor = source_name
                    break
        
        # If not found, use first monitor
        if not best_monitor and monitors:
            best_monitor = monitors[0][0]
        
        if best_monitor:
            print(f"✓ Found monitor source: {best_monitor}")
            
            # Set as default source
            if cls.set_default_source(best_monitor):
                print("✓ Set as default audio source")
                
                # Also set environment variable for this session
                os.environ['PULSE_SOURCE'] = best_monitor
                
                print(f"\n💡 To make this permanent, add to ~/.bashrc:")
                print(f"   export PULSE_SOURCE='{best_monitor}'")
                
                return True
            else:
                print("⚠️  Could not set default source, but will try to use it")
                os.environ['PULSE_SOURCE'] = best_monitor
                return True
        
        return False


class AudioCapture:
    """Handles real-time audio capture from system output"""
    
    def __init__(self, sample_rate: int = 16000, chunk_duration: float = 30.0,
                 device: Optional[int] = None):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_samples = int(sample_rate * chunk_duration)
        self.device = device
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.stream = None
        self.buffer = np.array([], dtype=np.float32)
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream - runs in separate thread"""
        if status:
            print(f"⚠️  Audio status: {status}")
        
        # Convert to mono if stereo
        if len(indata.shape) > 1:
            audio_data = indata.mean(axis=1)
        else:
            audio_data = indata.flatten()
        
        self.buffer = np.append(self.buffer, audio_data)
        
        # Check if we have enough data for a chunk
        while len(self.buffer) >= self.chunk_samples:
            chunk = self.buffer[:self.chunk_samples]
            self.buffer = self.buffer[self.chunk_samples:]
            self.audio_queue.put(chunk.copy())
    
    def start_capture(self):
        """Start audio capture"""
        if self.is_recording:
            raise AudioCaptureError("Already recording")
        
        try:
            self.is_recording = True
            self.stream = sd.InputStream(
                device=self.device,
                samplerate=self.sample_rate,
                channels=1,
                callback=self._audio_callback,
                blocksize=int(self.sample_rate * 0.1)
            )
            self.stream.start()
            
            device_name = "default"
            if self.device is not None:
                device_name = sd.query_devices(self.device)['name']
            
            print(f"✓ Audio capture started")
            print(f"  Device: {device_name}")
            print(f"  Sample rate: {self.sample_rate} Hz")
            
        except Exception as e:
            self.is_recording = False
            raise AudioCaptureError(f"Failed to start audio capture: {e}")
    
    def stop_capture(self):
        """Stop audio capture"""
        if self.stream:
            self.is_recording = False
            self.stream.stop()
            self.stream.close()
            self.stream = None
            print("✓ Audio capture stopped")
    
    def get_audio_chunk(self, timeout: Optional[float] = None) -> Optional[np.ndarray]:
        """Get next audio chunk from queue"""
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None


class JapaneseWhisperTranscriber:
    """Handles Japanese transcription using optimized Whisper models"""
    
    MODELS = {
        'kotoba-v1.0': {
            'path': 'kotoba-tech/kotoba-whisper-v1.0',
            'type': 'transformers',
            'vram': '6GB',
            'quality': 'excellent',
            'description': 'Kotoba Whisper v1.0 (proven quality for Japanese)'
        },
        'kotoba-v2.0': {
            'path': 'kotoba-tech/kotoba-whisper-v2.0',
            'type': 'transformers',
            'vram': '6GB',
            'quality': 'best',
            'description': 'Kotoba Whisper v2.0 (latest, more training data)'
        },
        'anime-whisper': {
            'path': 'litagin/anime-whisper',
            'type': 'transformers',
            'vram': '6GB',
            'quality': 'best',
            'description': 'Anime Whisper (specialized for anime/games)'
        },
        'large-v3': {
            'path': 'large-v3',
            'type': 'faster-whisper',
            'vram': '10GB',
            'quality': 'excellent',
            'description': 'OpenAI Whisper Large v3 (general multilingual)'
        },
        'medium': {
            'path': 'medium',
            'type': 'faster-whisper',
            'vram': '5GB',
            'quality': 'very good',
            'description': 'OpenAI Whisper Medium (faster alternative)'
        }
    }
    
    def __init__(self, model_name: str = "kotoba-v1.0", device: str = "auto"):
        if model_name not in self.MODELS:
            raise ValueError(f"Unknown model: {model_name}. Choose from: {list(self.MODELS.keys())}")
        
        self.model_name = model_name
        self.model_info = self.MODELS[model_name]
        self.model_path = self.model_info['path']
        self.model_type = self.model_info['type']
        
        # Determine device
        if device == "auto":
            if torch.cuda.is_available():
                self.device = "cuda"
                print(f"✓ CUDA available: {torch.cuda.get_device_name(0)}")
                print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
            else:
                self.device = "cpu"
                print("⚠️  CUDA not available, using CPU (slower)")
        else:
            self.device = device
        
        # Initialize model
        self.model = None
        self.pipeline = None
        self.vad_model = None
        self._load_model()
        
        # Try to load VAD for better timestamp estimation
        self._load_vad()
    
    def _load_model(self):
        """Load the appropriate model"""
        print(f"\n📥 Loading model: {self.model_name}")
        print(f"   Path: {self.model_path}")
        print(f"   Type: {self.model_type}")
        
        if self.model_type == 'faster-whisper':
            self._load_faster_whisper()
        elif self.model_type == 'transformers':
            self._load_transformers()
        
        print("✓ Model loaded successfully\n")
    
    def _load_faster_whisper(self):
        """Load model using faster-whisper"""
        WhisperModel = lazy_import_faster_whisper()
        
        compute_type = "float16" if self.device == "cuda" else "int8"
        
        try:
            self.model = WhisperModel(
                self.model_path,
                device=self.device,
                compute_type=compute_type
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load faster-whisper model: {e}")
    
    def _load_transformers(self):
        """Load model using transformers pipeline"""
        pipeline = lazy_import_transformers()
        
        device_id = 0 if self.device == "cuda" else -1
        
        print(f"  Device ID: {device_id} ({'GPU' if device_id >= 0 else 'CPU'})")
        
        try:
            # For Kotoba and Anime-Whisper models
            # Note: return_timestamps="word" causes issues with some models
            # Using chunk-level timestamps instead
            self.pipeline = pipeline(
                "automatic-speech-recognition",
                model=self.model_path,
                device=device_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                return_timestamps=True  # Chunk-level timestamps (more stable)
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load transformers pipeline: {e}")
    
    def _load_vad(self):
        """Load Silero VAD for accurate speech timestamp detection"""
        try:
            print("📥 Loading Silero VAD for accurate timestamps...")
            vad_model, get_speech_timestamps = lazy_import_silero_vad()
            if vad_model is not None and get_speech_timestamps is not None:
                self.vad_model = vad_model
                self.get_speech_timestamps = get_speech_timestamps
                print("✓ VAD loaded successfully")
            else:
                print("⚠️  VAD not available, using character-based estimation")
                self.vad_model = None
                self.get_speech_timestamps = None
        except Exception as e:
            print(f"⚠️  Could not load VAD: {e}")
            print("   Using character-based timestamp estimation")
            self.vad_model = None
            self.get_speech_timestamps = None
    
    @classmethod
    def list_models(cls):
        """List available models"""
        print("\n" + "=" * 70)
        print("Available Japanese Whisper Models")
        print("=" * 70)
        
        print("\n📌 Japanese-Optimized Models (via Transformers):")
        for name in ['kotoba-v1.0', 'kotoba-v2.0', 'anime-whisper']:
            info = cls.MODELS.get(name, {})
            print(f"  {name:20} - {info['description']}")
            print(f"  {'':20}   VRAM: {info['vram']}, Quality: {info['quality']}")
        
        print("\n📌 General Models (via faster-whisper):")
        for name in ['large-v3', 'medium']:
            info = cls.MODELS.get(name, {})
            print(f"  {name:20} - {info['description']}")
            print(f"  {'':20}   VRAM: {info['vram']}, Quality: {info['quality']}")
        
        print("\n" + "=" * 70)
        print("Recommendations:")
        print("  • kotoba-v1.0: Proven quality, most reliable for Japanese")
        print("  • kotoba-v2.0: Latest, more training data (test vs v1.0)")
        print("  • anime-whisper: Best for anime/games/casual speech")
        print("  • large-v3: OpenAI's latest (good fallback)")
        print("  • medium: Faster alternative (if VRAM limited)")
        print("\n⚠️  All models require: pip install transformers accelerate")
        print("=" * 70 + "\n")
    
    def transcribe(self, audio: np.ndarray, start_time: float) -> List[SubtitleSegment]:
        """Transcribe audio chunk and return subtitle segments"""
        try:
            if self.model_type == 'faster-whisper':
                return self._transcribe_faster_whisper(audio, start_time)
            elif self.model_type == 'transformers':
                return self._transcribe_transformers(audio, start_time)
        except Exception as e:
            print(f"⚠️  Transcription error: {e}")
            return []
    
    def _transcribe_faster_whisper(self, audio: np.ndarray, 
                                   start_time: float) -> List[SubtitleSegment]:
        """Transcribe using faster-whisper"""
        segments, info = self.model.transcribe(
            audio,
            language="ja",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=400
            )
        )
        
        subtitle_segments = []
        for segment in segments:
            subtitle_segments.append(SubtitleSegment(
                index=len(subtitle_segments) + 1,
                start=start_time + segment.start,
                end=start_time + segment.end,
                text=segment.text
            ))
        
        return subtitle_segments
    
    def _is_hallucination(self, text: str) -> bool:
        """
        Detect if text is likely a Whisper hallucination.
        Returns True if text should be discarded.
        """
        if not text:
            return True
        
        # Remove whitespace for analysis
        clean = text.strip()
        
        if not clean:
            return True
        
        # 1. Too short / just punctuation or ellipsis
        if len(clean) <= 3:
            return True
        
        # Check if it's just punctuation/symbols
        punctuation_only = all(c in '。！？、,!?.…─ー・「」『』（）()～〜' for c in clean)
        if punctuation_only:
            return True
        
        # 2. Repeated character run > 4 (e.g., "ーーーーー" or "ああああ")
        import re
        if re.search(r'(.)\1{4,}', clean):
            return True
        
        # 3. Repeated pattern > 3 times (e.g., "ゾンゾンゾンゾン")
        if re.search(r'(.{1,3})\1{3,}', clean):
            return True
        
        # 4. Low unique character ratio (< 30% unique chars)
        unique_chars = len(set(clean))
        total_chars = len(clean)
        if total_chars > 10 and (unique_chars / total_chars) < 0.3:
            return True
        
        # 5. Known hallucination patterns
        hallucination_patterns = ['゛ー゛', 'ンンン', 'ダッダッ', 'フォフォ']
        for pattern in hallucination_patterns:
            if pattern in clean:
                return True
        
        return False
    
    def _transcribe_transformers(self, audio: np.ndarray, 
                                 start_time: float) -> List[SubtitleSegment]:
        """Transcribe using transformers pipeline with VAD-based timestamp alignment"""
        try:
            # Ensure audio is float32 and properly shaped
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            
            # Transcribe the FULL audio chunk (model needs context)
            result = self.pipeline(
                audio,
                return_timestamps=False  # We'll use VAD for timestamps
            )
            
            # Extract text
            if isinstance(result, dict):
                text = result.get("text", "").strip()
            elif isinstance(result, str):
                text = result.strip()
            else:
                text = ""
            
            # Check for hallucination at chunk level
            if self._is_hallucination(text):
                return []
            
            # Use VAD to detect speech segments
            speech_segments = self._detect_speech_segments(audio)
            
            if not speech_segments:
                # Fallback: single segment for full duration
                duration = len(audio) / 16000.0
                return [SubtitleSegment(
                    index=1,
                    start=start_time,
                    end=start_time + duration,
                    text=text
                )]
            
            # Simple approach: distribute text across speech segments proportionally by duration
            # Each speech segment gets a portion of the text based on its duration
            total_speech_duration = sum(end - start for start, end in speech_segments)
            total_chars = len(text)
            
            subtitle_segments = []
            char_position = 0
            
            for i, (seg_start, seg_end) in enumerate(speech_segments):
                seg_duration = seg_end - seg_start
                
                # Calculate how many characters this segment should get
                if i == len(speech_segments) - 1:
                    # Last segment gets remaining text
                    segment_text = text[char_position:]
                else:
                    # Proportional character count based on duration
                    char_count = int((seg_duration / total_speech_duration) * total_chars)
                    
                    # Try to break at a natural point (punctuation or space-like character)
                    end_pos = char_position + char_count
                    
                    # Look for a good break point nearby
                    best_break = end_pos
                    for offset in range(min(20, char_count // 2)):
                        # Check forward
                        if end_pos + offset < len(text):
                            c = text[end_pos + offset]
                            if c in '。！？、,!?.…─ー':
                                best_break = end_pos + offset + 1
                                break
                        # Check backward
                        if end_pos - offset > char_position:
                            c = text[end_pos - offset]
                            if c in '。！？、,!?.…─ー':
                                best_break = end_pos - offset + 1
                                break
                    
                    segment_text = text[char_position:best_break]
                    char_position = best_break
                
                segment_text = segment_text.strip()
                
                # Filter out hallucinations at segment level too
                if segment_text and not self._is_hallucination(segment_text):
                    subtitle_segments.append(SubtitleSegment(
                        index=len(subtitle_segments) + 1,
                        start=start_time + seg_start,
                        end=start_time + seg_end,
                        text=segment_text
                    ))
            
            return subtitle_segments
            
        except Exception as e:
            print(f"⚠️  Transformers transcription error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _detect_speech_segments(self, audio: np.ndarray) -> List[Tuple[float, float]]:
        """
        Use Silero VAD to detect actual speech segments in audio.
        Returns list of (start_time, end_time) tuples in seconds.
        """
        if self.vad_model is None or self.get_speech_timestamps is None:
            # No VAD available, return full audio as one segment
            duration = len(audio) / 16000.0
            return [(0, duration)]
        
        try:
            # Prepare audio for VAD (needs 16kHz, torch tensor)
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            
            audio_tensor = torch.from_numpy(audio)
            
            # Get speech timestamps from VAD
            # min_speech_duration_ms: minimum speech chunk duration
            # min_silence_duration_ms: minimum silence duration to split chunks
            speech_timestamps = self.get_speech_timestamps(
                audio_tensor,
                self.vad_model,
                sampling_rate=16000,
                min_speech_duration_ms=250,  # At least 0.25s of speech
                min_silence_duration_ms=300,  # 0.3s silence splits segments
                speech_pad_ms=100  # Pad speech segments by 100ms
            )
            
            # Convert frame indices to seconds
            segments = []
            for ts in speech_timestamps:
                start_sec = ts['start'] / 16000.0
                end_sec = ts['end'] / 16000.0
                segments.append((start_sec, end_sec))
            
            return segments if segments else [(0, len(audio) / 16000.0)]
            
        except Exception as e:
            print(f"⚠️  VAD detection error: {e}")
            # Fallback to full audio
            duration = len(audio) / 16000.0
            return [(0, duration)]
    
    def _split_into_sentences_with_vad(self, text: str, audio: np.ndarray, 
                                      start_time: float) -> List[SubtitleSegment]:
        """
        Split text into sentences and align with actual speech timestamps from VAD.
        This gives much more accurate timestamps than character-based estimation.
        """
        if not text.strip():
            return []
        
        # First, split text into sentences
        sentences = self._split_japanese_sentences(text)
        
        if not sentences:
            return []
        
        # Detect actual speech segments using VAD
        speech_segments = self._detect_speech_segments(audio)
        
        # If we have the same number of sentences and speech segments, align them
        if len(sentences) == len(speech_segments):
            segments = []
            for i, (sentence, (seg_start, seg_end)) in enumerate(zip(sentences, speech_segments)):
                segments.append(SubtitleSegment(
                    index=i + 1,
                    start=start_time + seg_start,
                    end=start_time + seg_end,
                    text=sentence
                ))
            return segments
        
        # If counts don't match, distribute sentences across speech segments
        # This is more complex but handles cases where multiple sentences are in one speech segment
        return self._align_sentences_to_speech(sentences, speech_segments, start_time)
    
    def _split_japanese_sentences(self, text: str) -> List[str]:
        """Split Japanese text into sentences."""
        import re
        
        # Japanese sentence endings: 。！？ and their full-width equivalents
        sentences = re.split(r'([。！？]+[」』）\)]*)', text)
        
        # Recombine sentences with their endings
        combined_sentences = []
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                sentence = (sentences[i] + sentences[i + 1]).strip()
                if sentence:
                    combined_sentences.append(sentence)
        # Add last part if exists and wasn't paired
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            combined_sentences.append(sentences[-1].strip())
        
        # If no proper splits found, split by comma for long text
        if len(combined_sentences) <= 1 and len(text) > 100:
            parts = re.split(r'([、,]+)', text)
            combined_sentences = []
            for i in range(0, len(parts) - 1, 2):
                if i + 1 < len(parts):
                    part = (parts[i] + parts[i + 1]).strip()
                    if part:
                        combined_sentences.append(part)
            if len(parts) % 2 == 1 and parts[-1].strip():
                combined_sentences.append(parts[-1].strip())
        
        # If still no splits, return as single sentence
        if not combined_sentences:
            combined_sentences = [text]
        
        return combined_sentences
    
    def _align_sentences_to_speech(self, sentences: List[str], 
                                   speech_segments: List[Tuple[float, float]], 
                                   start_time: float) -> List[SubtitleSegment]:
        """
        Align sentences to detected speech segments.
        Handles cases where number of sentences != number of speech segments.
        """
        if not sentences or not speech_segments:
            return []
        
        segments = []
        
        # Calculate total duration and character count
        total_duration = sum(end - start for start, end in speech_segments)
        total_chars = sum(len(s) for s in sentences)
        
        # Distribute sentences across speech time proportionally
        current_speech_idx = 0
        current_speech_start, current_speech_end = speech_segments[current_speech_idx]
        available_duration = current_speech_end - current_speech_start
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            
            # Estimate how much time this sentence needs
            char_ratio = len(sentence) / total_chars if total_chars > 0 else 1.0 / len(sentences)
            needed_duration = total_duration * char_ratio
            
            # If current speech segment has enough time, use it
            if needed_duration <= available_duration * 1.2:  # 20% tolerance
                segment_end = current_speech_start + min(needed_duration, available_duration)
                
                segments.append(SubtitleSegment(
                    index=len(segments) + 1,
                    start=start_time + current_speech_start,
                    end=start_time + segment_end,
                    text=sentence
                ))
                
                current_speech_start = segment_end
                available_duration = current_speech_end - current_speech_start
                
                # Move to next speech segment if current is exhausted
                if available_duration < 0.1 and current_speech_idx < len(speech_segments) - 1:
                    current_speech_idx += 1
                    current_speech_start, current_speech_end = speech_segments[current_speech_idx]
                    available_duration = current_speech_end - current_speech_start
            else:
                # Need to span multiple speech segments
                # Use the full current speech segment and move to next
                segments.append(SubtitleSegment(
                    index=len(segments) + 1,
                    start=start_time + current_speech_start,
                    end=start_time + current_speech_end,
                    text=sentence
                ))
                
                # Move to next speech segment
                if current_speech_idx < len(speech_segments) - 1:
                    current_speech_idx += 1
                    current_speech_start, current_speech_end = speech_segments[current_speech_idx]
                    available_duration = current_speech_end - current_speech_start
        
        return segments
    
    def _merge_short_segments(self, segments: List[SubtitleSegment], 
                             min_duration: float = 1.0) -> List[SubtitleSegment]:
        """Merge very short segments for better readability"""
        if not segments:
            return []
        
        merged = []
        current = segments[0]
        
        for next_seg in segments[1:]:
            current_duration = current.end - current.start
            gap = next_seg.start - current.end
            
            # Merge if current segment is too short and gap is small
            if current_duration < min_duration and gap < 0.5:
                # Merge into current
                current.end = next_seg.end
                current.text = current.text + " " + next_seg.text
            else:
                # Keep current and move to next
                merged.append(current)
                current = next_seg
        
        # Add the last segment
        merged.append(current)
        
        # Re-index
        for i, seg in enumerate(merged, 1):
            seg.index = i
        
        return merged


class SubtitleGenerator:
    """Main class coordinating audio capture and transcription"""
    
    def __init__(self, output_file: str, model_name: str = "kotoba-v1.0",
                 device: str = "auto", audio_device: Optional[int] = None,
                 chunk_duration: float = 30.0):
        self.output_file = Path(output_file)
        self.chunk_duration = chunk_duration
        
        # Initialize components
        self.audio_capture = AudioCapture(
            chunk_duration=chunk_duration,
            device=audio_device
        )
        self.transcriber = JapaneseWhisperTranscriber(
            model_name=model_name,
            device=device
        )
        
        # State
        self.is_running = False
        self.segment_counter = 0
        self.current_time = 0.0
        self.srt_file = None
        self.chunks_processed = 0
    
    def start(self):
        """Start subtitle generation"""
        print("\n" + "=" * 70)
        print("Japanese Real-Time Subtitle Generation")
        print("=" * 70)
        print(f"Output file: {self.output_file}")
        print(f"Model: {self.transcriber.model_name}")
        print(f"Chunk duration: {self.chunk_duration}s")
        print("=" * 70 + "\n")
        
        # Open output file
        self.srt_file = open(self.output_file, 'w', encoding='utf-8')
        
        # Start audio capture
        self.audio_capture.start_capture()
        self.is_running = True
        
        # Start processing loop in separate thread
        processing_thread = threading.Thread(
            target=self._processing_loop,
            daemon=False
        )
        processing_thread.start()
        
        print("🎙️  Recording... Press Ctrl+C to stop\n")
        print("NOTE: When stopping, remaining audio chunks will be processed.")
        print("      Please wait for completion to avoid losing data.\n")
        
        try:
            while self.is_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print("⚠️  Ctrl+C detected - Stopping gracefully...")
            print("=" * 70)
            self.stop()
            print("\nWaiting for processing thread to complete...")
            processing_thread.join(timeout=300)
            if processing_thread.is_alive():
                print("⚠️  Warning: Processing thread still running after timeout")
            else:
                print("✓ Processing thread completed")
    
    def _processing_loop(self):
        """Main processing loop - runs in separate thread"""
        try:
            while self.is_running:
                audio_chunk = self.audio_capture.get_audio_chunk(timeout=1.0)
                
                if audio_chunk is None:
                    continue
                
                self.chunks_processed += 1
                queue_size = self.audio_capture.audio_queue.qsize()
                
                status_msg = f"[{self._format_time(self.current_time)}] Processing chunk {self.chunks_processed}"
                if queue_size > 0:
                    status_msg += f" (Queue: {queue_size} chunks)"
                    if queue_size > 3:
                        status_msg += " ⚠️  FALLING BEHIND"
                
                print(status_msg)
                
                # Transcribe
                transcribe_start = time.time()
                segments = self.transcriber.transcribe(audio_chunk, self.current_time)
                transcribe_time = time.time() - transcribe_start
                
                # Write to SRT file
                for segment in segments:
                    self.segment_counter += 1
                    segment.index = self.segment_counter

                    self.srt_file.write(segment.to_srt())
                    self.srt_file.flush()

                    print(f"  [{self._format_time(segment.start)} --> "
                          f"{self._format_time(segment.end)}] {segment.text}", flush=True)
                
                if not segments:
                    print("  (No speech detected)")
                
                # Show processing performance
                processing_ratio = transcribe_time / self.chunk_duration
                if processing_ratio > 0.8:
                    print(f"  ⏱️  Processing took {transcribe_time:.1f}s for "
                          f"{self.chunk_duration:.0f}s audio (ratio: {processing_ratio:.2f})")
                
                self.current_time += self.chunk_duration
                print()
            
            # Process remaining chunks
            self._process_remaining_chunks()
            
        except Exception as e:
            print(f"\n❌ Error in processing loop: {e}")
            import traceback
            traceback.print_exc()
    
    def _process_remaining_chunks(self):
        """Process any remaining chunks in the queue after stopping"""
        remaining = self.audio_capture.audio_queue.qsize()
        if remaining > 0:
            print(f"\n{'=' * 70}")
            print(f"Processing {remaining} remaining audio chunk(s)...")
            print("Please wait - this ensures no audio is lost!")
            print("=" * 70 + "\n")
            
            chunk_num = 0
            while not self.audio_capture.audio_queue.empty():
                chunk_num += 1
                audio_chunk = self.audio_capture.get_audio_chunk(timeout=0.1)
                if audio_chunk is not None:
                    print(f"Processing remaining chunk {chunk_num}/{remaining}...")
                    segments = self.transcriber.transcribe(audio_chunk, self.current_time)
                    
                    for segment in segments:
                        self.segment_counter += 1
                        segment.index = self.segment_counter
                        self.srt_file.write(segment.to_srt())
                        self.srt_file.flush()
                        print(f"  [{self._format_time(segment.start)} --> "
                              f"{self._format_time(segment.end)}] {segment.text}", flush=True)
                    
                    if not segments:
                        print("  (No speech detected)")
                    
                    self.current_time += self.chunk_duration
                    print()
            
            print(f"✓ All {remaining} remaining chunk(s) processed!")
    
    def stop(self):
        """Stop subtitle generation"""
        if not self.is_running:
            return
        
        print("\nStopping audio capture...")
        self.is_running = False
        self.audio_capture.stop_capture()
        
        if self.srt_file:
            self.srt_file.close()
        
        print(f"\n{'=' * 70}")
        print("FINAL STATISTICS")
        print("=" * 70)
        print(f"✓ Subtitles saved to: {self.output_file}")
        print(f"  Total segments: {self.segment_counter}")
        print(f"  Total duration: {self._format_time(self.current_time)}")
        print(f"  Chunks processed: {self.chunks_processed}")
        print("=" * 70)
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format time for display"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


def main():
    parser = argparse.ArgumentParser(
        description='Japanese Real-Time Audio Subtitle Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Command-Line Recording:
  Record and transcribe audio in real-time from your terminal.
  The transcription will be saved to an SRT subtitle file.

  Basic usage:
    livecaption --model kotoba-v1.0 --output my_recording.srt

  Then:
    1. Start playing audio (YouTube, Netflix, local video, etc.)
    2. Press Ctrl+C to stop recording
    3. Find your subtitles in my_recording.srt

  The transcription appears in real-time in your terminal and is
  automatically saved to the SRT file.

Examples:
  # Use Kotoba Whisper v1.0 (proven quality for Japanese)
  livecaption --model kotoba-v1.0 --output subs.srt

  # Use Kotoba Whisper v2.0 (latest Japanese model)
  livecaption --model kotoba-v2.0 --output subs.srt

  # Use Anime Whisper (best for anime/games)
  livecaption --model anime-whisper --output anime_subs.srt

  # Use Whisper Large v3 (multilingual - 99+ languages)
  livecaption --model large-v3 --output english_subs.srt

  # Use CPU instead of GPU (slower but no GPU required)
  livecaption --device cpu --output subs.srt

  # List available models and their details
  livecaption --list-models

  # Custom chunk duration (faster processing, less context)
  livecaption --model kotoba-v1.0 --chunk-duration 15 --output subs.srt

First-Time Setup:
  After installing via pip, you MUST run the setup command:
    livecaption-setup

  This will:
    • Register the native messaging host for Firefox
    • Detect available audio sources
    • Configure model cache directory
    • Set up Firefox extension integration

Firefox Extension:
  Install the LiveCaption extension from Firefox Add-ons:
    https://addons.mozilla.org/firefox/addon/livecaption/

  Then click the extension icon to use the browser interface.

Uninstallation:
  To completely remove LiveCaption:
    livecaption-uninstall

  This will remove:
    • Native messaging host (~/.mozilla/native-messaging-hosts/)
    • Configuration files (~/.config/livecaption/)
    • Python package (via pip)

  You can also uninstall manually:
    python -m livecaption.uninstaller

Audio Setup (Linux/PipeWire):
  The script will automatically detect and configure your audio source.
  If auto-detection fails, manually run:
    pactl list sources | grep -i monitor
    export PULSE_SOURCE='your_monitor_source_name'
        """
    )
    
    parser.add_argument('--output', '-o', default='subtitles.srt',
                       help='Output SRT file path (default: subtitles.srt)')
    parser.add_argument('--model', '-m', default='kotoba-v1.0',
                       choices=['kotoba-v1.0', 'kotoba-v2.0', 'anime-whisper', 'large-v3', 'medium'],
                       help='Model to use (default: kotoba-v1.0)')
    parser.add_argument('--device', '-d', default='auto',
                       choices=['auto', 'cuda', 'cpu'],
                       help='Device to use for inference (default: auto)')
    parser.add_argument('--audio-device', '-a', type=int, default=None,
                       help='Audio device index (usually auto-detected)')
    parser.add_argument('--chunk-duration', '-c', type=float, default=30.0,
                       help='Audio chunk duration in seconds (default: 30.0)')
    parser.add_argument('--list-models', action='store_true',
                       help='List available models and exit')
    parser.add_argument('--skip-audio-setup', action='store_true',
                       help='Skip automatic audio source configuration')
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_models:
        JapaneseWhisperTranscriber.list_models()
        return 0
    
    # Auto-configure audio source (unless skipped)
    if not args.skip_audio_setup:
        if not PulseAudioManager.auto_configure_audio():
            print("\n⚠️  Audio auto-configuration failed!")
            print("You may need to manually configure your audio source.\n")
            response = input("Continue anyway? (y/N): ").strip().lower()
            if response != 'y':
                return 1
    
    # Create and start generator
    try:
        generator = SubtitleGenerator(
            output_file=args.output,
            model_name=args.model,
            device=args.device,
            audio_device=args.audio_device,
            chunk_duration=args.chunk_duration
        )
        generator.start()
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())