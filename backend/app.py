from flask import Flask, request, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "../Resources"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process', methods=['POST'])
def process_video():
    file = request.files['video']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    filename = secure_filename('carLicence4.mp4')  # name it what your script expects
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        subprocess.run([
            'python',
            '../yolov10/anpr.py'
        ], check=True)

        return jsonify({'success': True})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
