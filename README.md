# AI News Automation Pipeline - GTA VI Edition

A production-ready, fully automated AI News Bot that generates YouTube Shorts from latest GTA VI news sources. Runs completely on GitHub Actions without requiring local machine uptime.

## Features

- 🔄 **Automated News Collection**: Runs every 30 minutes via GitHub Actions
- 🎥 **YouTube Shorts Generation**: Automatically creates 30-45 second videos daily
- 🤖 **AI-Powered Content**: Uses OpenRouter API for intelligent script writing
- 🎙️ **Free TTS**: Generates voice narration without paid services
- 📝 **Modular Architecture**: Single responsibility principle for each module
- 🔒 **Production Ready**: Error handling, logging, and retry mechanisms

## News Sources

- Google News RSS (GTA VI)
- Rockstar Newswire
- RockstarINTEL
- Reddit r/GTA6
- IGN Gaming
- GameRant
- Dexerto Gaming

## Architecture

```
├── sources.py           # News collection from multiple sources
├── deduplicator.py      # Filtering and deduplication
├── writer.py            # AI script generation via OpenRouter
├── tts.py              # Text-to-Speech synthesis
├── editor.py           # Video editing with FFmpeg
├── uploader.py         # Metadata preparation & upload support
├── bot.py              # Orchestration pipeline
├── config.py           # Configuration management
├── logger.py           # Logging setup
└── .github/workflows/
    ├── news_collection.yml    # Runs every 30 minutes
    └── video_generation.yml   # Runs daily
```

## Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/himanshumeena671-code/Ai-News-Bot.git
cd Ai-News-Bot
pip install -r requirements.txt
```

### 2. Set Environment Variables

Add these to GitHub Secrets:

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### 3. Configure GitHub Actions

- News collection runs every 30 minutes
- Video generation runs daily
- Results stored in GitHub and ready for upload

## Usage

### Local Testing

```bash
# Test news collection
python bot.py --collect-news

# Test script generation
python bot.py --generate-script

# Full pipeline
python bot.py --run-full
```

### Automatic Execution

Push to main branch and GitHub Actions handles everything.

## Tech Stack

- **Python 3.9+**
- **FFmpeg**: Video composition
- **Requests**: HTTP operations
- **Feedparser**: RSS parsing
- **BeautifulSoup4**: Web scraping
- **OpenRouter API**: AI models
- **Google Text-to-Speech**: Free TTS
- **GitHub Actions**: Orchestration

## Project Status

🚀 **Production Deployment Ready**

## License

MIT

## Support

For issues and feature requests, open a GitHub issue.
