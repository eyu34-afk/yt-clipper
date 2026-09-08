import os
from flask import Flask, render_template, request, send_file, jsonify
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
        return jsonify({'error': 'Please provide a valid YouTube URL.'}), 400

    output_filename = 'output_clip.mp4'
    
    # Clean up any leftover clip from previous runs
    if os.path.exists(output_filename):
        os.remove(output_filename)

    section_range = f"*{start_time}-{end_time}"

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'download_sections': [section_range],
        'outtmpl': output_filename,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_filename):
            return send_file(output_filename, as_attachment=True)
        else:
            return jsonify({'error': 'Failed to generate the video clip.'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)