import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clip', methods=['POST'])
def clip_video():
    url = request.form.get('url')
    start_time = request.form.get('start_time', '00:00:00')
    end_time = request.form.get('end_time', '00:00:30')

    if not url:
        return {'error': 'URL is required'}, 400

    output_path = 'output_clip.mp4'
    if os.path.exists(output_path):
        os.remove(output_path)

    # Definitive yt-dlp configuration to bypass cloud bot checks
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'cookiefile': 'cookies.txt',
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'android']
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True)
        else:
            return {'error': 'Clip generation failed - file not found'}, 500

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)