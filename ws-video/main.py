from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from PIL import Image, ImageOps
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    print(f'received message: {data}')
    emit('response', {'data': f'Server received: {data}'}, broadcast=True)

@socketio.on('frame')
def handle_frame(data):
    print('Received frame')
    image_data = data['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))

    # Transform colors of the image
    image = transform_colors(image)

    # Convert the image back to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Send the image back to the client
    emit('image_response', {'image': f'data:image/png;base64,{image_base64}'}, broadcast=True)

def transform_colors(image):
    # Example transformation: convert image to grayscale and apply a blue tint
    grayscale_image = ImageOps.grayscale(image)
    tinted_image = ImageOps.colorize(grayscale_image, black="black", white="blue")
    return tinted_image

if __name__ == '__main__':
    socketio.run(app)
