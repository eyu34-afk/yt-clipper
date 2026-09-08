import os
import subprocess
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_clip():
    url = request.form.get('url')
    start = request.form.get('start')  # Format: mm:ss or hh:mm:ss
    end = request.form.get('end')      # Format: mm:ss or hh:mm:ss
    
    output_filename = "output_clip.mp4"
    
    # Clean up old file if it exists
    if os.path.exists(output_filename):
        os.remove(output_filename)

    section_arg = f"*{start}-{end}"
    command = [
        "yt-dlp",
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / mp4",
        "--download-sections", section_arg,
        "-o", output_filename,
        url
    ]
    
    try:
        # Execute the download command on the server
        subprocess.run(command, check=True)
        
        if os.path.exists(output_filename):
            return send_file(output_filename, as_attachment=True)
        else:
            return "Error: Clip could not be generated.", 500
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)