from flask import Flask, request, render_template, Response
import socket
import time
import json
import threading
import subprocess
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'total-bot-war-secret-key'

HOST = "localhost"
lock = threading.Lock()


def valid_user():
    user = request.headers.get('X-Game-Identifier')
    valid = True if user is not None and user == 'TotalBotWarClient' else False
    return valid


@app.route("/", methods=["GET"])
def Index():
    return render_template('index.html')


def get_available_port():
    for puerto in range(1024, 65535):
        try:
            # Intenta conectarse al puerto
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((HOST, puerto))
                # Si ha llegado aquí es que se ha podido conectar
                return puerto
        except:
            pass
    return None


@app.route("/game/start")
def start_game():
    # Validar el usuario
    if (not valid_user()): return "Acces not allowed", 403

    bot0 = request.args.get("bot0")
    bot1 = request.args.get("bot1")

    screen_width = request.args.get("width")
    screen_height = request.args.get("height")

    print(f"Screen width: {screen_width}")
    print(f"Screen height: {screen_height}")

    print(bot0)
    print(bot1)
    # Generar id único para el usuario
    ID = uuid.uuid4()
    print(f"Client id: {ID}")

    global puerto, lock
    # Para prevenir condiciones de carrera
    with lock:
        port = None
        while not port:

            # Buscar un puerto disponible
            port = get_available_port()
            print(f"Trying with port {port}")
            # Crear proceso secundario
            try:
                # Creamos el proceso hijo
                proceso = subprocess.Popen(
                    ['python', '../executor.py', HOST, str(port), str(ID), bot0, bot1, str(screen_width), str(screen_height)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                # Espera la respuesta del hijo
                socket_state = proceso.stdout.readline().decode().strip()
            except:
                socket_state = "ERROR"

            # Si el hijo no ha podido establecer la conexión con el socket
            if socket_state != "READY": port = None
    print(f"Proceso escuchando en {HOST} puerto {port}")

    # Devolver mensaje con info en caso de que t0d0 haya ido bien y error en caso contrario y gestionarlo desde unity

    # Devuelve la información necesaria para que el cliente gestione la conexión al socket
    return json.dumps({"host": HOST, "port": port, "id": str(ID)}), 200


@app.route("/game/start/test")
def start_game_test():
    # Validar el usuario
    if (not valid_user()): return "Acces not allowed", 403

    # Generar id único para el usuario
    ID = uuid.uuid4()
    print(f"Client id: {ID}")

    # Buscar un puerto disponible
    port = get_available_port()

    # Devuelve la información necesaria para que el cliente gestione la conexión al socket
    return json.dumps({"host": HOST, "port": port, "id": str(ID)}), 200


if __name__ == "__main__":
    app.run(debug=True, port=4000)