from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)

app.static_folder = "static"

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/video", methods=["GET", "POST"])
def video():
    if request.method == "POST":
        uploaded_file = request.files["video"]

        video_path = os.path.join('uploads', "input_file.mp4")
        uploaded_file.save(video_path)
        compressed_path = 'static/compressed_video.mp4'
        compress_video(video_path, compressed_path)

        original_file_size = os.path.getsize(video_path)
        compressed_file_size = os.path.getsize(compressed_path)
        ori_size_mb = original_file_size / 1000000
        compress_size_mb = compressed_file_size / 1000000

        return render_template(
            "index.html",
            compressed_video=compressed_path,
            original_size=ori_size_mb,
            compressed_size=compress_size_mb,
        )
    return render_template("index.html")

def compress_video(input_file, output_file):
    cap = cv2.VideoCapture(input_file, cv2.CAP_FFMPEG)
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    codec = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, codec, fps, (frame_width, frame_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    cap.release()
    out.release()

if __name__ == "__main__":
    app.run(debug=True)
