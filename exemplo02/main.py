from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit
import subprocess

# Cria uma instância do Flask
app = Flask(__name__)

# Cria uma instância do SocketIO - ele é utilizado para enviar mensagens para o cliente utilizando websockets
socketio = SocketIO(app,debug=True,cors_allowed_origins='*',async_mode='eventlet')

# Rota principal
@app.route('/home')
def main():
        return render_template('index.html')

# Inicia o servidor de WebSocket
@socketio.on("my_event")
def checkping():
    for x in range(5):
        # Comando para verificar o ping
        cmd = 'ping -c 1 8.8.8.8|head -2|tail -1'
        # Roda um comando no shell e retorna a saída
        # Com o parâmetro text=True, a saída é retornada como string. O subprocess.run() retorna um objeto do tipo subprocess.CompletedProcess
        listing1 = subprocess.run(cmd,stdout=subprocess.PIPE,text=True,shell=True)
        # Envia a saída do comando para o cliente
        # O request.sid é o identificador da sessão do cliente. Ele está disponível em todos os eventos do SocketIO
        sid = request.sid
        # Envia a mensagem para o cliente. A função emit() envia a mensagem para o cliente. O primeiro parâmetro é o nome do evento, o segundo é o dado a ser enviado e o terceiro é o identificador do cliente
        emit('server', {"data1":x, "data":listing1.stdout}, room=sid)
        socketio.sleep(1)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5006)