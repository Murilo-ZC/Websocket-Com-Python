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

@socketio.on('image')
def handle_image(data):
    print('Received image')
    image_data = data['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    image.save('received_image.png')
    
    # Retorna a imagem para o cliente

    # Converte as cores da imagem
    image = transform_colors(image)
    
    # Convert the image back to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")

    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Send the image back to the client
    emit('image_response', {'image': f'data:image/png;base64,{image_base64}'}, broadcast=True)

# Função para trocar a cor da imagem
def transform_colors(image):
    # Example transformation: convert image to grayscale and apply a blue tint
    grayscale_image = ImageOps.grayscale(image)
    tinted_image = ImageOps.colorize(grayscale_image, black="black", white="blue")
    return tinted_image

if __name__ == '__main__':
    socketio.run(app)
