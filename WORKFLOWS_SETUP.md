# GitHub Actions Workflows Setup Guide

## Overview

This project uses GitHub Actions to automate the entire AI News Bot pipeline. Two workflows are configured:

1. **News Collection** - Runs every 30 minutes
2. **Video Generation** - Runs daily

## Setup Instructions

### Step 1: Create Secrets

Go to your repository Settings → Secrets and add:

- `OPENROUTER_API_KEY` - Your OpenRouter API key (get from https://openrouter.ai)
- `GITHUB_TOKEN` - Automatically provided by GitHub (optional, used for releases)

### Step 2: Enable Workflows

1. Go to Actions tab
2. Enable workflows if they're disabled
3. Workflows will start automatically on schedule

### Step 3: Manual Trigger

You can manually trigger workflows:

```bash
# Trigger news collection
gh workflow run news_collection.yml

# Trigger video generation
gh workflow run video_generation.yml
```

## Workflow 1: News Collection (`news_collection.yml`)

**Trigger:** Every 30 minutes (or manual)

**What it does:**
1. Collects GTA VI news from all sources
2. Saves raw news to `raw_news.json`
3. Commits and pushes updates to repository
4. Uploads artifacts for review

**Configuration:**
```yaml
schedule:
  - cron: '*/30 * * * *'  # Every 30 minutes
```

## Workflow 2: Video Generation (`video_generation.yml`)

**Trigger:** Daily at 8 AM UTC (or manual)

**What it does:**
1. Runs complete pipeline:
   - Filter and deduplicate news
   - Generate AI scripts
   - Create text-to-speech audio
   - Compose YouTube Shorts videos
2. Uploads videos as releases
3. Commits final metadata

**Configuration:**
```yaml
schedule:
  - cron: '0 8 * * *'  # Daily at 8 AM UTC
```

**Also triggers on:**
- Push to `raw_news.json`
- Push to `requirements.txt`
- Push to `bot.py`

## Required Environment Setup

### In .env (for local testing):
```
OPENROUTER_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

### In GitHub Secrets:
- `OPENROUTER_API_KEY` - Required for AI script generation

## Artifacts Generated

### News Collection Workflow
- `raw_news.json` - All collected articles (7 day retention)

### Video Generation Workflow
- `video_output/` - Generated MP4 files
- `upload_staging/` - Upload metadata and scripts
- `final_content.json` - Complete content packages
- GitHub Release - Video files tagged with date

## Monitoring Workflows

### Check Status
1. Go to Actions tab
2. Click on workflow run
3. View logs and artifacts

### Common Issues

**API Key Error:**
- Ensure `OPENROUTER_API_KEY` is set in Secrets
- Check it's valid: https://openrouter.ai

**FFmpeg Not Found:**
- Workflows install FFmpeg automatically
- For local testing: `sudo apt-get install ffmpeg`

**Permission Denied:**
- Ensure GitHub token permissions allow pushes
- Check branch protection rules

## Manual Workflow Files

If you need to create the workflow files manually:

### `.github/workflows/news_collection.yml`

```yaml
name: News Collection
on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  collect-news:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          pip install -r requirements.txt
          python bot.py --collect-news
      - uses: actions/upload-artifact@v3
        with:
          name: raw-news
          path: raw_news.json
```

### `.github/workflows/video_generation.yml`

```yaml
name: Video Generation
on:
  schedule:
    - cron: '0 8 * * *'
  workflow_dispatch:
  push:
    paths:
      - 'raw_news.json'

jobs:
  generate-videos:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg
          pip install -r requirements.txt
          python bot.py --run-full
      - uses: actions/upload-artifact@v3
        with:
          name: generated-content
          path: |
            video_output/
            upload_staging/
            final_content.json
```

## Testing Workflows Locally

### Option 1: GitHub CLI
```bash
gh workflow run video_generation.yml
```

### Option 2: Act (Local Simulation)
```bash
# Install act: https://github.com/nektos/act
act -j generate-videos
```

### Option 3: Manual Testing
```bash
python bot.py --run-full
```

## Cost Considerations

### GitHub Actions
- **Free tier:** 2,000 minutes/month
- **News collection:** ~2 min per run × 48 runs/day = 96 min/day = ~3,000 min/month
- **Video generation:** ~10 min per run × 1 run/day = ~10 min/day = ~300 min/month
- **Total:** ~3,300 min/month (exceeds free tier slightly)

**Recommendations:**
- Reduce news collection frequency to hourly: `0 * * * *`
- Or run video generation only 3x per week
- Adjust cron expressions based on your needs

### OpenRouter API
- **Pricing:** Variable by model
- **Free tier:** Limited (check their website)
- **Cost:** ~$0.01-0.10 per video (depends on model)

## Secrets Management

### Security Best Practices
1. **Never commit API keys** to repository
2. **Use GitHub Secrets** for sensitive data
3. **Rotate keys regularly**
4. **Monitor API usage** for anomalies

### View Secret Usage
```bash
# Check which workflows use secrets (in logs)
# Secrets are masked in logs for security
```

## Workflow Optimization

### Reduce Execution Time
1. Limit articles processed: Edit `config.py`
2. Use faster TTS provider
3. Parallelize video generation (future enhancement)

### Reduce API Costs
1. Increase deduplication threshold
2. Process fewer articles per day
3. Use batch endpoints if available

## Troubleshooting

### Workflow Fails to Start
- Check cron syntax: https://crontab.guru
- Verify scheduled workflows are enabled

### API Rate Limits
- Add delays between requests
- Reduce batch size
- Use exponential backoff

### FFmpeg Errors
- Ensure video format is supported
- Check audio codec compatibility
- Verify file paths are correct

## Next Steps

1. ✅ Set `OPENROUTER_API_KEY` secret
2. ✅ Push to repository
3. ✅ Monitor first workflow run (Actions tab)
4. ✅ Adjust cron schedules as needed
5. ✅ Check generated videos in Releases

## Support

For workflow issues:
- Check Action logs for error messages
- Review OpenRouter API status
- Verify FFmpeg installation
- Test pipeline locally first

---

**Generated by AI News Bot Setup**
