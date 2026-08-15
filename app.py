from flask import Flask, render_template, jsonify, send_from_directory
import os
import random
import socket
from cartas_data import buscar_significado

app = Flask(__name__, template_folder='.')

CARDS_FOLDER = os.path.join(os.path.dirname(__file__), 'imagenes_cartas')

def index():
    return render_template('index.html')

def get_cartas():
    """Devuelve 5 cartas aleatorias con su significado."""
    archivos = [f for f in os.listdir(CARDS_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    seleccion = random.sample(archivos, min(5, len(archivos)))
    resultado = []
    for archivo in seleccion:
        invertida = random.random() < 0.5
        sig = buscar_significado(archivo)
        resultado.append({
            "archivo": archivo,
            "invertida": invertida,
            "nombre": sig.get("nombre", archivo),
            "numero": sig.get("numero", ""),
            "palo": sig.get("palo", "Arcano Mayor"),
            "significado": sig.get("invertida" if invertida else "normal", "")
        })
    return jsonify(resultado)

def serve_card(filename):
    return send_from_directory(CARDS_FOLDER, filename)

app.add_url_rule('/', 'index', index)
app.add_url_rule('/cartas', 'get_cartas', get_cartas)
app.add_url_rule('/imagenes_cartas/<filename>', 'serve_card', serve_card)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

if __name__ == '__main__':
    port = 5000
    ip = get_local_ip()
    print(f'\n  Tarot Mistico')
    print(f'  Local  -> http://127.0.0.1:{port}')
    print(f'  Red    -> http://{ip}:{port}\n')
    app.run(host='0.0.0.0', port=port, debug=True)