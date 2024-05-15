# Utilizando WebSockets com Python

Pessoal vamos utilizar neste exemplo o Python para criar um servidor WebSocket e um cliente WebSocket.
Primeiro vamos avaliar alguns pontos importantes para que essa comunicação possa acontecer.

## O que é WebSocket?

Observem a figura abaixo:

<img src="https://www-uploads.scaleway.com/blog-websockets-bigger-4.webp"/>

O que temos aqui de importante para observarmos:

- Quando estamos falando de comunicação HTTP, o cliente faz uma requisição para o servidor e o servidor responde. A comunicação é encerrada após a resposta do servidor.
- Quando estamos utilizando WebSocket, a comunicação é mantida aberta entre o cliente e o servidor. O cliente pode enviar mensagens para o servidor e o servidor pode enviar mensagens para o cliente.

> Mas Murilo, como isso é possível?

O WebSocket é um protocolo de comunicação que permite a comunicação bidirecional entre o cliente e o servidor. O protocolo é baseado em TCP e possui um handshake que é feito através de uma requisição HTTP.

<img src="https://koenig-media.raywenderlich.com/uploads/2020/08/Screenshot_2020-08-10_at_15.08.19.png"/>

O procedimento para a comunicação é o seguinte:

1. O cliente faz uma requisição HTTP para o servidor solicitando a atualização do protocolo para WebSocket.
2. O servidor responde com um cabeçalho de resposta que indica que a atualização do protocolo foi aceita.
3. A partir desse momento a comunicação é feita através do protocolo WebSocket.
4. A troca de mensagens é feita através de mensagens binárias ou mensagens de texto. Elas são enviadas através de frames. Cada frame possui um cabeçalho que indica o tipo da mensagem e o tamanho da mensagem.
5. A comunicação é mantida aberta até que uma das partes decida encerrar a conexão.

Para saber mais:

<iframe width="560" height="315" src="https://www.youtube.com/embed/1BfCnjr_Vjg?si=2kpCnB42ymuf2gVx" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/pnj3Jbho5Ck?si=Yt1sPm7L_Dgthxdq" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<iframe width="560" height="315" src="https://www.youtube.com/embed/8ARodQ4Wlf4?si=PZW1XvkxT6gVJpLq" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Criando um servidor WebSocket

Vamos criar um servidor WebSocket em conjunto com um servidor Flask. O servidor Flask será responsável por servir a página HTML que contém o código JavaScript que fará a comunicação com o servidor WebSocket.

***IMPORTANTE:*** Lembrem-se de criar os ambientes virtuais para fazer a instalação das dependências.

```bash
python3 -m venv venv
source venv/bin/activate
```

Vamos instalar as dependências:

```bash
pip install Flask
pip install Flask-SocketIO
```

## Código do servidor WebSocket

```python
# Importamos o Flask e o SocketIO
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Criamos a aplicação Flask
app = Flask(__name__)

# Configuramos a chave secreta. Ela é utilizada para criptografar as mensagens.
app.config['SECRET_KEY'] = 'secret!'

# Criamos o objeto SocketIO passando a aplicação Flask
socketio = SocketIO(app)

# Definimos a rota principal. Nela que vamos renderizar a página HTML
@app.route('/')
def index():
    return render_template('index.html')
 
# Definimos o evento de mensagem. Quando o cliente enviar uma mensagem, o servidor vai receber e enviar uma resposta.
# Existem outros eventos do SocketIO que podem ser utilizados. Alguns exemplos são: connect, disconnect, message, etc.
@socketio.on('message')
def handle_message(data):
    print(f'received message: {data}')
    emit('response', {'data': f'Server received: {data}'  }, broadcast=True)

# Iniciamos o servidor SocketIO
# É possível iniciar o servidor SocketIO em uma porta diferente da porta do servidor Flask
# Para isso, basta passar o parâmetro port para o método run
if __name__ == '__main__':
    socketio.run(app)
```

## Código do cliente WebSocket

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Example</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
    <script type="text/javascript">
        document.addEventListener('DOMContentLoaded', function() {
            var socket = io();

            socket.on('connect', function() {
                socket.send('User has connected!');
            });

            socket.on('response', function(data) {
                document.getElementById('messages').innerHTML += '<br>' + data.data;
            });

            document.getElementById('sendButton').onclick = function() {
                var text = document.getElementById('myMessage').value;
                socket.send(text);
                document.getElementById('myMessage').value = '';
            };

            // Adiciona envio dos comandos para cada um dos botões
            document.getElementById('upButton').onclick = function() {
                var text = {"msg":"Vai para Cima!", "command":"up"};
                socket.send(text);
            };

            document.getElementById('downButton').onclick = function() {
                var text = {"msg":"Vai para Baixo!", "command":"down"};
                socket.send(text);
            };

            document.getElementById('leftButton').onclick = function() {
                var text = {"msg":"Vai para Esquerda!", "command":"left"};
                socket.send(text);
            };

            document.getElementById('rightButton').onclick = function() {
                var text = {"msg":"Vai para Direita!", "command":"right"};
                socket.send(text);
            };
        });
    </script>
</head>
<body>
    <h1>WebSocket Communication</h1>
    <input type="text" id="myMessage">
    <button id="sendButton">Send</button>
    <button id="upButton">Up</button>
    <button id="downButton">Down</button>
    <button id="leftButton">Left</button>
    <button id="rightButton">Right</button>
    <div id="messages"></div>
</body>
</html>

```

## Desafios de Hoje

1. Criar um servidor WebSocket que consiga utilizar o HTMX para a comunicação com o cliente.
2. Criar um servidor WebSocket que consiga lidar com imagens. O cliente deve enviar uma imagem para o servidor e o servidor deve enviar a imagem de volta para o cliente, com as cores invertidas.