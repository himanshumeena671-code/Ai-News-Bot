# 🤖 AI News Bot - Automated YouTube Shorts Generator

Transform GTA VI news into viral YouTube Shorts automatically using AI, TTS, and FFmpeg.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 🎯 Overview

**AI News Bot** is a fully automated pipeline that:

1. **Collects** GTA VI news from 7+ sources
2. **Filters** duplicate and low-quality content
3. **Generates** viral titles, hooks, and scripts using AI
4. **Creates** text-to-speech narration
5. **Produces** professional YouTube Shorts videos
6. **Prepares** metadata for upload

All with zero manual intervention! 🚀

## ✨ Features

- ✅ **Multi-source news collection** (Google News, Rockstar, Reddit, IGN, GameRant, etc.)
- ✅ **AI-powered script generation** using OpenRouter API
- ✅ **Professional TTS narration** (Google TTS & pyttsx3)
- ✅ **Video production** with FFmpeg (1080x1920 YouTube Shorts format)
- ✅ **Automated deduplication** with ML-based similarity detection
- ✅ **GitHub Actions CI/CD** for scheduled execution
- ✅ **Upload-ready metadata** with YouTube description templates
- ✅ **Modular architecture** for easy customization
- ✅ **Comprehensive logging** for debugging

## 🏗️ Architecture

```
AI News Bot Pipeline
├── Phase 1: News Collection (sources.py)
│   └── 7+ news sources → raw_news.json
├── Phase 2: Filtering (deduplicator.py)
│   └── Duplicate removal, relevance check → filtered_news.json
├── Phase 3: Script Generation (writer.py)
│   └── AI-powered titles, hooks, scripts → content_packages.json
├── Phase 4: TTS Generation (tts.py)
│   └── Text-to-speech audio → audio_output/
├── Phase 5: Video Creation (editor.py)
│   └── Compose videos with subtitles → video_output/
└── Phase 6: Upload Preparation (uploader.py)
    └── Metadata & scripts → upload_staging/
```

## 🚀 Quick Start

### Prerequisites

```bash
# System dependencies
sudo apt-get update
sudo apt-get install -y python3.9 ffmpeg

# Python 3.9+
python3 --version
```

### Installation

```bash
# Clone repository
git clone https://github.com/himanshumeena671-code/Ai-News-Bot.git
cd Ai-News-Bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=your_api_key_here
LOG_LEVEL=INFO
EOF

# Get OpenRouter API key:
# 1. Visit https://openrouter.ai
# 2. Sign up free
# 3. Create API key
# 4. Add to .env
```

### Run Pipeline

```bash
# Full pipeline (all phases)
python bot.py --run-full

# Run specific phases
python bot.py --collect-news          # Phase 1 only
python bot.py --up-to-scripts         # Phases 1-3
python bot.py --up-to-videos          # Phases 1-5
```

## 📊 Pipeline Output

After running the full pipeline:

```
ai-news-bot/
├── raw_news.json                 # Phase 1: Raw articles
├── filtered_news.json            # Phase 2: Filtered articles
├── content_packages.json         # Phase 3: Generated scripts
├── content_with_audio.json       # Phase 4: With audio paths
├── final_content.json            # Phase 5: Complete content
├── audio_output/
│   ├── gta6_short_1.mp3
│   ├── gta6_short_2.mp3
│   └── ...
├── video_output/
│   ├── gta6_short_1.mp4          # 1080x1920, 45s
│   ├── gta6_short_2.mp4
│   └── ...
├── upload_staging/
│   ├── upload_batch.json         # Upload metadata
│   ├── upload.py                 # YouTube API script
│   └── UPLOAD_INSTRUCTIONS.md
└── logs/
    └── ai_news_bot_*.log
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Processing
MAX_ARTICLES_TO_PROCESS = 5          # Videos per run
MAX_SOURCES = 7                       # News sources
SIMILARITY_THRESHOLD = 0.85           # Deduplication

# Video
VIDEO_WIDTH = 1080                    # Shorts format
VIDEO_HEIGHT = 1920
VIDEO_DURATION = 45                   # seconds
VIDEO_BITRATE = "5000k"

# TTS
TTS_PROVIDER = 'gtts'                 # or 'pyttsx3'
TTS_SPEED = 1.0

# Directories
AUDIO_OUTPUT_DIR = "audio_output"
VIDEO_OUTPUT_DIR = "video_output"
```

## 🤖 AI Integration

The bot uses **OpenRouter API** with free/cheap models:

- **Model:** Meta Llama 2 7B (free tier available)
- **Cost:** ~$0.01-0.10 per video
- **Features Used:**
  - Viral title generation
  - Hook creation
  - Script writing
  - Hashtag generation

### API Usage Example

```python
from writer import AIScriptWriter

writer = AIScriptWriter(api_key="your_api_key")
title = writer.generate_viral_title("GTA VI News", "Trailer dropped")
# Output: "🔴 LEAKED GTA6 FOOTAGE GOES VIRAL! 🚨"
```

## 📱 Generated Content Example

**Input Article:**
```
"Rockstar announces GTA VI release date"
```

**Generated Output:**
```
Title:     "🚨 GTA 6 OFFICIAL RELEASE DATE REVEALED! 2024 HYPE! 🔴"
Hook:      "Rockstar just dropped the biggest news in gaming..."
Script:    "After months of speculation, Rockstar Games has officially..."
Hashtags:  #GTA6 #GrandTheftAuto #Gaming #News #2024Release
Duration:  45 seconds (YouTube Shorts format)
```

## 🔄 Automation with GitHub Actions

### Setup

1. Go to Repository → Settings → Secrets
2. Add `OPENROUTER_API_KEY`
3. Workflows start automatically!

### Workflows

**News Collection** (every 30 minutes)
```yaml
schedule:
  - cron: '*/30 * * * *'
```

**Video Generation** (daily at 8 AM UTC)
```yaml
schedule:
  - cron: '0 8 * * *'
```

See [WORKFLOWS_SETUP.md](WORKFLOWS_SETUP.md) for details.

## 📤 Upload to YouTube

### Automated Upload

```bash
# Generate upload script
python -c "from uploader import UploadManager; UploadManager().load_and_prepare_upload()"

# Configure credentials
# Edit: upload_staging/upload.py
# Add: Google OAuth credentials

# Run upload
python upload_staging/upload.py
```

### Manual Upload

1. Go to [YouTube Studio](https://studio.youtube.com)
2. Use metadata from `upload_batch.json`
3. Videos in `video_output/`

See [UPLOAD_INSTRUCTIONS.md](upload_staging/UPLOAD_INSTRUCTIONS.md) for details.

## 📊 Project Structure

```
ai-news-bot/
├── sources.py              # Phase 1: News collection
├── deduplicator.py         # Phase 2: Filtering & dedup
├── writer.py               # Phase 3: AI script generation
├── tts.py                  # Phase 4: Text-to-speech
├── editor.py               # Phase 5: Video editing
├── uploader.py             # Phase 6: Upload preparation
├── config.py               # Configuration
├── logger.py               # Logging setup
├── bot.py                  # Master orchestration
├── requirements.txt        # Dependencies
├── .env                    # Local config (git ignored)
├── README.md              # This file
└── .github/workflows/
    ├── news_collection.yml
    └── video_generation.yml
```

## 🧪 Testing

### Test Individual Phases

```python
# Test news collection
from sources import NewsCollector
collector = NewsCollector()
articles = collector.collect_all_news()

# Test deduplication
from deduplicator import NewsDuplicator
dedup = NewsDuplicator()
filtered = dedup.filter_articles(articles)

# Test script generation
from writer import AIScriptWriter
writer = AIScriptWriter()
packages = writer.process_multiple_articles(filtered)
```

### Run with Verbose Logging

```bash
LOG_LEVEL=DEBUG python bot.py --run-full
```

## 📈 Performance

| Phase | Duration | CPU | Memory |
|-------|----------|-----|--------|
| Collection | 2-5m | Low | Low |
| Filtering | 1m | Low | Low |
| Script Gen | 5-10m | Medium | Medium |
| TTS | 3-5m | Low | Low |
| Video | 5-10m | High | High |
| **Total** | **20-30m** | Medium | Medium |

## 🔐 Security

- ✅ API keys stored in `.env` (git ignored)
- ✅ No credentials in logs
- ✅ Environment variables for CI/CD
- ✅ Input validation & sanitization
- ✅ Error handling & rate limiting

## 🐛 Troubleshooting

### Common Issues

**"OPENROUTER_API_KEY not found"**
```bash
# Check .env file exists and has valid key
cat .env | grep OPENROUTER
```

**"FFmpeg not found"**
```bash
# Install FFmpeg
sudo apt-get install -y ffmpeg
ffmpeg -version
```

**"No articles collected"**
- Check internet connection
- Verify news sources are accessible
- Check logs: `tail -f logs/*.log`

**"API rate limit exceeded"**
- Reduce `MAX_ARTICLES_TO_PROCESS`
- Increase delay between requests
- Check OpenRouter account limits

## 📚 Documentation

- [WORKFLOWS_SETUP.md](WORKFLOWS_SETUP.md) - GitHub Actions guide
- [config.py](config.py) - Configuration reference
- [bot.py](bot.py) - Main orchestration

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Thumbnail generation with PIL
- [ ] Multi-language support
- [ ] Custom background videos
- [ ] Advanced video effects
- [ ] Analytics integration
- [ ] Reddit auto-posting
- [ ] TikTok integration

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

## ⭐ Show Your Support

If this project helped you, please ⭐ star it on GitHub!

## 🚀 Roadmap

- v1.1: Thumbnail generation
- v1.2: Multi-language support
- v1.3: Custom video templates
- v1.4: Analytics dashboard
- v2.0: Web UI for configuration

## 📞 Support

- 🐛 Report bugs: [Issues](https://github.com/himanshumeena671-code/Ai-News-Bot/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/himanshumeena671-code/Ai-News-Bot/discussions)
- 📧 Email: himanshumeena671@gmail.com

## 🙏 Acknowledgments

- OpenRouter for AI API
- FFmpeg for video processing
- gTTS for text-to-speech
- Feedparser for RSS feeds
- All news sources for content

---

**Made with ❤️ by Himanshu Meena**

Last Updated: July 2026
