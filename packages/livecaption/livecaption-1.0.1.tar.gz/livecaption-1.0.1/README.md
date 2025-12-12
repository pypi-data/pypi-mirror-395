# 🎙️ LiveCaption

**Real-time audio transcription for video streaming with Firefox browser integration**

LiveCaption captures system audio and transcribes it in real-time using state-of-the-art Whisper models. Perfect for Japanese anime, streaming content, and multilingual videos.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Firefox](https://img.shields.io/badge/firefox-91+-orange.svg)

## ✨ Features

- **Real-time transcription** - See subtitles as you watch
- **Firefox integration** - One-click recording from browser toolbar
- **Multiple Whisper models**:
  - **Kotoba Whisper v2.0** - Best for Japanese (recommended)
  - **Whisper Large v3** - Best for English and 99+ other languages
  - **Anime Whisper** - Specialized for anime/games
- **SRT output** - Standard subtitle format for video players
- **Voice Activity Detection** - Accurate timestamp alignment
- **Command-line & browser modes** - Use from terminal or Firefox extension

## 📋 System Requirements

- **Operating System**: Linux (tested on Fedora, Ubuntu)
- **Browser**: Firefox 91+ (for browser extension)
- **Audio System**: PipeWire or PulseAudio
- **Python**: 3.9 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: NVIDIA GPU recommended (~4GB VRAM), CPU mode available

## 🚀 Installation

### Method 1: pip (Recommended)

```bash
pip install livecaption
livecaption-setup
```

**Note**: After `pip install`, you **must** run `livecaption-setup` to register the Firefox native messaging host.

### Method 2: From Source

```bash
git clone https://github.com/b-tok/LiveCaption.git
cd LiveCaption
./install.sh
```

### First-Time Model Download
- AI models are 1-6GB each and download on first use
- First download takes 5-30 minutes depending on internet speed
- Models are cached locally for subsequent runs

## 📖 Usage

### Browser Extension

1. **Install Firefox Extension**:
   - [Firefox Add-ons Store](https://addons.mozilla.org/firefox/addon/LiveCaption/) (recommended)
   - Or download `.xpi` from [GitHub Releases](https://github.com/b-tok/LiveCaption/releases)

2. **Click the LiveCaption icon** in Firefox toolbar
3. **Select your settings**:
   - Model: `kotoba-v2.0` for Japanese, `large-v3` for English
   - Audio Source: Usually auto-detected
   - Output File: Where to save the SRT (default: `~/Documents/LiveCaption/recording_<timestamp>.srt`)
4. **Click "Start Recording"** and play your video
5. **Click "Stop Recording"** to save the SRT file

### Command Line

```bash
# Basic usage (Japanese content)
livecaption --model kotoba-v2.0 --output subtitles.srt

# English/multilingual content
livecaption --model large-v3 --output subtitles.srt

# Anime/games (Japanese)
livecaption --model anime-whisper --output anime.srt

# List all available models
livecaption --list-models

# Get help
livecaption --help
```

**Workflow**:
1. Run the command
2. Start playing audio (YouTube, Netflix, local video, etc.)
3. Press Ctrl+C to stop recording
4. Find your subtitles in the output file

## ⚙️ Models

| Model | Best For | Size | Languages | Recommended Use |
|-------|----------|------|-----------|-----------------|
| `kotoba-v2.0` | Japanese | ~4GB | Japanese | **Best for Japanese content** |
| `large-v3` | Multilingual | ~6GB | 99+ languages | **Best for English/other languages** |
| `anime-whisper` | Anime/Games | ~4GB | Japanese | Anime, visual novels, games |
| `kotoba-v1.0` | Japanese | ~4GB | Japanese | Older, more stable |
| `medium` | Fast | ~3GB | Multilingual | Faster but less accurate |

**Recommendation**: Use `kotoba-v2.0` for Japanese, `large-v3` for everything else.

## 🗑️ Uninstallation

```bash
# Complete uninstall (recommended)
livecaption-uninstall

# Alternative method
python -m livecaption.uninstaller
```

**Note**: Manually remove the Firefox extension from `about:addons` if installed.

## 📝 Configuration

Settings are stored in `~/.config/livecaption/config.json`:

```json
{
  "language": "ja",
  "model": "kotoba-v2.0",
  "device": "auto",
  "output_dir": "~/Documents/LiveCaption",
  "chunk_duration": 30.0
}
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Kotoba-Whisper](https://huggingface.co/kotoba-tech/kotoba-whisper-v2.0) - Japanese-optimized Whisper
- [Anime-Whisper](https://huggingface.co/anime-whisper) - Anime-specialized model
- [OpenAI Whisper](https://github.com/openai/whisper) - Base transcription model
- [Silero VAD](https://github.com/snakers4/silero-vad) - Voice activity detection
