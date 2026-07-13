"""
Phase 5: Upload Module
Prepares metadata and handles upload operations.
Single Responsibility: Manage upload preparation and future API integration.
"""

import logging
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class UploadManager:
    """Manages video upload metadata and preparation."""
    
    def __init__(self, output_dir: str = "upload_staging"):
        """
        Initialize upload manager.
        
        Args:
            output_dir: Directory to stage files for upload
        """
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.info("Upload Manager initialized")
    
    def prepare_upload_metadata(self, content_package: Dict) -> Dict:
        """
        Prepare complete metadata for upload.
        
        Args:
            content_package: Content package with all generated files
            
        Returns:
            Upload-ready metadata dictionary
        """
        try:
            metadata = {
                'title': content_package.get('viral_title', 'GTA VI News'),
                'description': content_package.get('description', ''),
                'tags': content_package.get('hashtags', []),
                'video_file': content_package.get('video_path', ''),
                'thumbnail_text': content_package.get('hook', '')[:50],
                'category': 'Gaming',
                'made_for_kids': False,
                'privacy_status': 'public',
                'original_source': content_package.get('original_source', ''),
                'original_link': content_package.get('original_link', ''),
                'generated_at': content_package.get('generated_at', ''),
                'ready_for_upload': os.path.exists(content_package.get('video_path', '')),
                'metadata_created_at': datetime.now().isoformat()
            }
            
            logger.info(f"Prepared metadata for: {metadata['title']}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error preparing metadata: {str(e)}")
            return {}
    
    def create_upload_batch(self, content_packages: List[Dict]) -> List[Dict]:
        """
        Create upload metadata for multiple videos.
        
        Args:
            content_packages: List of content packages
            
        Returns:
            List of upload-ready metadata dictionaries
        """
        logger.info(f"Preparing {len(content_packages)} packages for upload...")
        
        upload_batch = []
        
        for package in content_packages:
            if package.get('video_generated'):
                metadata = self.prepare_upload_metadata(package)
                if metadata.get('ready_for_upload'):
                    upload_batch.append(metadata)
        
        logger.info(f"Batch ready: {len(upload_batch)} videos prepared for upload")
        return upload_batch
    
    def save_upload_batch(self, metadata_list: List[Dict], filename: str = "upload_batch.json") -> bool:
        """
        Save upload batch to JSON file.
        
        Args:
            metadata_list: List of metadata dictionaries
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_list, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved batch metadata to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving batch metadata: {str(e)}")
            return False
    
    def generate_thumbnail_placeholder(self, title: str, filename: str) -> Optional[str]:
        """
        Generate placeholder thumbnail metadata.
        For full implementation, use PIL to create actual thumbnails.
        
        Args:
            title: Video title
            filename: Thumbnail filename
            
        Returns:
            Path to thumbnail metadata file
        """
        try:
            # For now, just create metadata. Full implementation would use PIL
            thumbnail_data = {
                'title': title,
                'filename': filename,
                'created_at': datetime.now().isoformat(),
                'note': 'Placeholder - generate actual thumbnail with PIL or similar'
            }
            
            output_path = os.path.join(self.output_dir, filename + '.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(thumbnail_data, f, indent=2)
            
            logger.info(f"Created thumbnail metadata: {filename}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating thumbnail: {str(e)}")
            return None
    
    def create_youtube_upload_script(self, metadata_list: List[Dict], output_file: str = "upload.py") -> bool:
        """
        Create a Python script template for YouTube API uploads.
        Users can fill in credentials and run manually or in CI/CD.
        
        Args:
            metadata_list: List of upload metadata
            output_file: Output script filename
            
        Returns:
            True if successful
        """
        try:
            script_content = '''#!/usr/bin/env python3
"""
YouTube Upload Script
Use this to upload prepared videos to YouTube.
Requires: google-auth-oauthlib, google-auth-httplib2, google-api-python-client
"""

import json
import sys
from datetime import datetime

# Uncomment to use actual YouTube API
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

def load_metadata(filename="upload_batch.json"):
    """Load upload metadata."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return []

def upload_to_youtube(title, description, video_file, tags):
    """Upload video to YouTube.
    
    Args:
        title: Video title
        description: Video description
        video_file: Path to video file
        tags: List of tags
    
    Returns:
        Video ID if successful, None otherwise
    """
    try:
        # TODO: Implement actual YouTube API upload
        # This is a template for future implementation
        
        print(f"\n[DEMO] Would upload:")
        print(f"  Title: {title}")
        print(f"  File: {video_file}")
        print(f"  Tags: {', '.join(tags)}")
        print(f"  Status: Ready for actual upload")
        
        # Actual implementation:
        # youtube = build('youtube', 'v3', credentials=credentials)
        # request = youtube.videos().insert(
        #     part='snippet,status',
        #     body={
        #         'snippet': {
        #             'title': title,
        #             'description': description,
        #             'tags': tags,
        #             'categoryId': '20'  # Gaming category
        #         },
        #         'status': {'privacyStatus': 'public'}
        #     },
        #     media_body=MediaFileUpload(video_file, mimetype='video/mp4')
        # )
        # response = request.execute()
        # return response['id']
        
        return "DEMO_VIDEO_ID"
        
    except Exception as e:
        print(f"Error uploading video: {e}")
        return None

def main():
    """Main upload function."""
    metadata_list = load_metadata()
    
    if not metadata_list:
        print("No videos to upload")
        return
    
    print(f"\nPrepared to upload {len(metadata_list)} videos")
    print("\n" + "="*60)
    
    successful = 0
    failed = 0
    
    for i, metadata in enumerate(metadata_list, 1):
        print(f"\n[{i}/{len(metadata_list)}] Uploading: {metadata['title']}")
        
        if not metadata.get('ready_for_upload'):
            print("  Status: Not ready for upload")
            failed += 1
            continue
        
        video_id = upload_to_youtube(
            title=metadata.get('title'),
            description=metadata.get('description'),
            video_file=metadata.get('video_file'),
            tags=metadata.get('tags', [])
        )
        
        if video_id:
            successful += 1
            print(f"  Status: ✓ Uploaded (ID: {video_id})")
        else:
            failed += 1
            print(f"  Status: ✗ Upload failed")
    
    print(f"\n" + "="*60)
    print(f"Upload Summary: {successful} successful, {failed} failed")
    print(f"\nNext steps:")
    print(f"1. Add YouTube API credentials to this script")
    print(f"2. Run: python {__file__}")
    print(f"3. Videos will be uploaded to your YouTube channel")

if __name__ == "__main__":
    main()
'''
            
            output_path = os.path.join(self.output_dir, output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            os.chmod(output_path, 0o755)  # Make executable
            logger.info(f"Created upload script: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating upload script: {str(e)}")
            return False
    
    def create_upload_readme(self, output_file: str = "UPLOAD_INSTRUCTIONS.md") -> bool:
        """
        Create README with upload instructions.
        
        Args:
            output_file: Output filename
            
        Returns:
            True if successful
        """
        try:
            readme_content = '''# YouTube Upload Instructions

## Overview

Your AI-generated YouTube Shorts are ready for upload. This guide explains how to upload them to YouTube.

## Generated Files

- `upload_batch.json` - Metadata for all videos
- `upload.py` - Python script for automated uploads
- Video files in `video_output/` directory

## Setup YouTube API

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as JSON

### Step 2: Install Dependencies

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 3: Modify Upload Script

Edit `upload.py` and:
1. Add your credentials file path
2. Implement the `upload_to_youtube()` function
3. Set privacy status (public/private/unlisted)

### Step 4: Run Upload Script

```bash
python upload.py
```

## Manual Upload (Alternative)

1. Go to [YouTube Studio](https://studio.youtube.com)
2. Click "Create" → "Upload Videos"
3. Select videos from `video_output/`
4. Copy title and description from `upload_batch.json`
5. Add tags from the metadata
6. Click "Publish"

## Batch Upload Tools

Consider using:
- **VidIQ Creator Studio** - Bulk upload with scheduling
- **YouTube Studio API** - Programmatic upload (recommended)
- **TubeBuddy** - Analytics and bulk operations

## Upload Schedule

Recommended posting times for gaming content:
- **Weekdays**: 3-5 PM (viewer engagement)
- **Weekends**: 12-3 PM (peak gaming hours)
- **Frequency**: 2+ videos per day for algorithm boost

## Important Notes

⚠️ **Verify Before Upload**
- Check video quality and duration (should be ~45 seconds)
- Confirm audio is audible and synced
- Review title, description, and tags
- Test with unlisted video first

⚠️ **YouTube Policies**
- Original content (AI-generated summaries are OK)
- No clickbait titles
- Accurate descriptions
- Proper attribution to news sources
- No misleading thumbnails

## Troubleshooting

**Video won't upload**
- Check file format (must be MP4)
- Verify file size < 256GB
- Ensure credentials are valid

**Metadata issues**
- Title must be < 100 characters
- Description < 5000 characters
- Tags must be ASCII text

**API errors**
- Refresh OAuth token
- Check quota limits
- Verify YouTube account is in good standing

## Next Steps

1. Set up YouTube API credentials
2. Run upload script or use YouTube Studio
3. Monitor analytics and engagement
4. Adjust script/content based on performance
5. Automate with GitHub Actions for daily uploads

## Support

For issues:
- Check YouTube API documentation
- Review error logs in script output
- Verify video files exist and are readable

---

*Generated by AI News Bot*
'''
            
            output_path = os.path.join(self.output_dir, output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            logger.info(f"Created upload instructions: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating readme: {str(e)}")
            return False
    
    def load_and_prepare_upload(self, input_file: str = "final_content.json") -> List[Dict]:
        """
        Load final content and prepare for upload.
        
        Args:
            input_file: Input JSON file with final content
            
        Returns:
            List of upload-ready metadata dictionaries
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                packages = json.load(f)
            
            logger.info(f"Loaded {len(packages)} packages for upload preparation")
            
            # Create upload batch
            upload_batch = self.create_upload_batch(packages)
            
            # Save batch
            self.save_upload_batch(upload_batch)
            
            # Create helper scripts and documentation
            self.create_youtube_upload_script(upload_batch)
            self.create_upload_readme()
            
            logger.info(f"Upload preparation complete: {len(upload_batch)} videos ready")
            return upload_batch
            
        except Exception as e:
            logger.error(f"Error in load_and_prepare_upload: {str(e)}")
            return []


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the upload manager
    try:
        manager = UploadManager()
        upload_batch = manager.load_and_prepare_upload()
        
        print(f"\nUpload batch prepared: {len(upload_batch)} videos")
        for video in upload_batch:
            print(f"\n📤 {video['title']}")
            print(f"   Status: Ready for upload")
            print(f"   Tags: {', '.join(video['tags'][:3])}...")
    except Exception as e:
        print(f"Error: {e}")
