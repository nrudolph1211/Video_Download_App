# Video Downloader - YouTube, Instagram, Facebook & TikTok

A simple and elegant web application for downloading videos from YouTube, Instagram, Facebook, and TikTok in high quality MP4 format, optimized for Premiere Pro compatibility.

## Features

- 🎥 Download YouTube videos in highest quality (up to 1080p)
- 📸 Download Instagram videos and reels in high quality
- 📘 Download Facebook videos in high quality
- 🎵 Download TikTok videos in high quality
- 📁 MP4 format for Premiere Pro compatibility
- 🌐 Modern, responsive web interface with tab navigation
- ⚡ Real-time download progress tracking
- 🔒 Safe and secure downloads
- 📱 Mobile-friendly design

## Prerequisites

Before running the application, make sure you have:

1. **Python 3.7+** installed on your system
2. **yt-dlp** installed (will be installed automatically via requirements.txt)

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/nathanielrudolph/Desktop/YT DOWNLOAD APP"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install yt-dlp (if not already installed):**
   ```bash
   pip install yt-dlp
   ```

## Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open your web browser and go to:**
   ```
   http://localhost:8080
   ```

3. **Download videos:**
   - Choose between YouTube, Instagram, Facebook, or TikTok tabs
   - Copy any video URL from the selected platform
   - Paste it into the text field
   - Click "Download Video"
   - Wait for the download to complete
   - Click the download link to save the file

## Supported URL Formats

### YouTube:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&t=42s` (with timestamp)

### Instagram:
- `https://www.instagram.com/p/POST_ID/`
- `https://www.instagram.com/reel/REEL_ID/`
- `https://instagram.com/p/POST_ID/`

### Facebook:
- `https://www.facebook.com/watch/?v=VIDEO_ID`
- `https://fb.watch/VIDEO_ID/`
- `https://www.facebook.com/video.php?v=VIDEO_ID`

### TikTok:
- `https://www.tiktok.com/@username/video/VIDEO_ID`
- `https://vm.tiktok.com/VIDEO_ID/`
- `https://tiktok.com/@username/video/VIDEO_ID`

## Download Settings

The application is configured to:
- Download videos in the highest quality available (up to 1080p)
- Convert to MP4 format for maximum compatibility
- Optimize for Premiere Pro editing software
- Save files to the `downloads/` folder

## File Locations

- **Downloaded videos:** `/Users/nathanielrudolph/Desktop/YT DOWNLOAD APP/downloads/`
- **Web interface:** `http://localhost:8080`
- **Application logs:** Check terminal output

## Troubleshooting

### Common Issues

1. **"yt-dlp command not found"**
   - Make sure yt-dlp is installed: `pip install yt-dlp`
   - Try updating yt-dlp: `pip install --upgrade yt-dlp`

2. **Download fails**
   - Check your internet connection
   - Verify the YouTube URL is correct
   - Some videos may be restricted or unavailable

3. **Port 8080 already in use**
   - Stop other applications using port 8080
   - Or modify the port in `app.py` (line 174)

### Updating yt-dlp

YouTube, Instagram, Facebook, and TikTok frequently change their systems, so it's important to keep yt-dlp updated:

```bash
pip install --upgrade yt-dlp
```

## Technical Details

- **Backend:** Flask (Python web framework)
- **Video Downloader:** yt-dlp (YouTube, Instagram, Facebook, and TikTok downloader)
- **Frontend:** HTML5, CSS3, JavaScript with tab navigation
- **File Format:** MP4 (H.264 codec)
- **Quality:** Best available (up to 1080p)

## License

This project is for educational purposes. Please respect YouTube's, Instagram's, Facebook's, and TikTok's Terms of Service and copyright laws when downloading content.

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Make sure all dependencies are installed
3. Verify your internet connection
4. Try updating yt-dlp to the latest version
