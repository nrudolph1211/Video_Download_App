from flask import Flask, request, jsonify, send_file, render_template
import subprocess
import os
import tempfile
import threading
import time
from pathlib import Path
import json

app = Flask(__name__)

# Configuration
DOWNLOAD_DIR = "/tmp/downloads"  # Use /tmp for Railway compatibility
MAX_CONCURRENT_DOWNLOADS = 3

# Create downloads directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Store active downloads
active_downloads = {}

@app.route('/health')
def health_check():
    # Allow healthcheck requests from Railway
    return jsonify({'status': 'healthy', 'service': 'video-downloader'}), 200

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback HTML if template is missing
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Video Downloader</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
                .container { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); text-align: center; max-width: 600px; }
                h1 { color: #333; margin-bottom: 20px; }
                .status { color: #666; margin-bottom: 20px; }
                .download-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 16px; cursor: pointer; margin: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎥 Video Downloader</h1>
                <p class="status">YouTube, Instagram, Facebook & TikTok</p>
                <p>Template file is missing. Please upload templates/index.html to GitHub.</p>
                <p><strong>Error:</strong> {}</p>
                <button class="download-btn" onclick="alert('Upload templates/index.html to fix this!')">Fix Required</button>
            </div>
        </body>
        </html>
        '''.format(str(e)), 200

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url', '').strip()
    platform = data.get('platform', 'youtube')  # Default to YouTube
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL based on platform
    if platform == 'youtube':
        if 'youtube.com' not in url and 'youtu.be' not in url:
            return jsonify({'error': 'Please provide a valid YouTube URL'}), 400
    elif platform == 'instagram':
        if 'instagram.com' not in url:
            return jsonify({'error': 'Please provide a valid Instagram URL'}), 400
    elif platform == 'facebook':
        if 'facebook.com' not in url and 'fb.watch' not in url:
            return jsonify({'error': 'Please provide a valid Facebook URL'}), 400
    elif platform == 'tiktok':
        if 'tiktok.com' not in url:
            return jsonify({'error': 'Please provide a valid TikTok URL'}), 400
    
    # Generate unique download ID
    download_id = f"download_{int(time.time())}_{len(active_downloads)}"
    
    # Start download in background thread
    thread = threading.Thread(target=download_video_thread, args=(url, download_id, platform))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'download_id': download_id,
        'status': 'started',
        'message': 'Download started successfully'
    })

def download_video_thread(url, download_id, platform='youtube'):
    """Download video in background thread"""
    try:
        # Initialize download status
        active_downloads[download_id] = {
            'status': 'downloading',
            'progress': 0,
            'filename': '',
            'error': None,
            'platform': platform
        }
        
        # yt-dlp command with optimal settings for Premiere Pro compatibility
        cmd = [
            'yt-dlp',
            '--format', 'best[height<=1080]/best',  # Prefer 1080p or best available
            '--merge-output-format', 'mp4',          # Ensure MP4 output
            '--output', f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            '--progress', '--newline',
            '--no-playlist',  # Only download single video
            '--ignore-errors',  # Continue on download errors
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '--referer', 'https://www.youtube.com/',
            '--sleep-requests', '1',
            '--sleep-interval', '1',
            url
        ]
        
        # Run yt-dlp and capture output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        output_lines = []
        for line in process.stdout:
            output_lines.append(line.strip())
            
            # Extract progress information
            if '[download]' in line and '%' in line:
                try:
                    # Extract percentage from yt-dlp output
                    percent_start = line.find('[') + 1
                    percent_end = line.find('%')
                    if percent_start > 0 and percent_end > percent_start:
                        percent_str = line[percent_start:percent_end]
                        percent = float(percent_str.split()[-1])
                        active_downloads[download_id]['progress'] = min(100, percent)
                except:
                    pass
            
            # Extract filename
            if 'Destination:' in line:
                filename = line.split('Destination:')[-1].strip()
                active_downloads[download_id]['filename'] = os.path.basename(filename)
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code == 0:
            # Find the downloaded file
            downloaded_files = []
            for file in os.listdir(DOWNLOAD_DIR):
                if file.endswith(('.mp4', '.webm', '.mkv')):
                    downloaded_files.append(file)
            
            if downloaded_files:
                # Get the most recently downloaded file
                latest_file = max(downloaded_files, key=lambda f: os.path.getctime(os.path.join(DOWNLOAD_DIR, f)))
                active_downloads[download_id]['status'] = 'completed'
                active_downloads[download_id]['progress'] = 100
                active_downloads[download_id]['filename'] = latest_file
            else:
                active_downloads[download_id]['status'] = 'error'
                active_downloads[download_id]['error'] = 'No video file found after download'
        else:
            # Capture error output for debugging
            error_output = '\n'.join(output_lines[-10:])  # Last 10 lines
            
            # Check if it's a YouTube bot detection error
            if 'Sign in to confirm you\'re not a bot' in error_output or 'bot' in error_output.lower():
                active_downloads[download_id]['status'] = 'error'
                active_downloads[download_id]['error'] = 'YouTube is blocking automated downloads. Try again later or use a different video.'
            else:
                active_downloads[download_id]['status'] = 'error'
                active_downloads[download_id]['error'] = f'Download failed with return code {return_code}. Output: {error_output}'
            
    except Exception as e:
        active_downloads[download_id]['status'] = 'error'
        active_downloads[download_id]['error'] = str(e)

@app.route('/status/<download_id>')
def get_download_status(download_id):
    if download_id not in active_downloads:
        return jsonify({'error': 'Download not found'}), 404
    
    return jsonify(active_downloads[download_id])

@app.route('/download_file/<download_id>')
def download_file(download_id):
    if download_id not in active_downloads:
        return jsonify({'error': 'Download not found'}), 404
    
    download_info = active_downloads[download_id]
    if download_info['status'] != 'completed':
        return jsonify({'error': 'Download not completed'}), 400
    
    filename = download_info['filename']
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(file_path, as_attachment=True, download_name=filename)

@app.route('/list_downloads')
def list_downloads():
    """List all completed downloads"""
    downloads = []
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith(('.mp4', '.webm', '.mkv')):
            file_path = os.path.join(DOWNLOAD_DIR, file)
            downloads.append({
                'filename': file,
                'size': os.path.getsize(file_path),
                'created': os.path.getctime(file_path)
            })
    
    # Sort by creation time (newest first)
    downloads.sort(key=lambda x: x['created'], reverse=True)
    
    return jsonify(downloads)

if __name__ == '__main__':
    # Railway injects PORT environment variable - use it for health checks
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
