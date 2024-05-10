from flask import Flask, render_template
from flask_socketio import SocketIO, Namespace, emit
import cv2
import base64
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

class VideoNamespace(Namespace):
    def on_connect(self):
        print("Connected to video channel")
        self.send_video_frames()

    def send_video_frames(self):
        cap = cv2.VideoCapture('Aula01.mkv')  # Substitua com o caminho do seu vídeo
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            emit('video_frame', {'data': frame_base64})
            time.sleep(0.033)  # Controla a taxa de frame enviada; ajuste conforme necessário
        cap.release()
        emit('video_end', {'data': 'Video transmission complete'})

socketio.on_namespace(VideoNamespace('/video'))

@app.route('/video')
def index():
    return render_template('dois.html')

if __name__ == '__main__':
    socketio.run(app)
