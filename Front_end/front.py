from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
from flask_caching import Cache
import pickle

app = Flask(__name__, template_folder='./')
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração básica do cache (memória neste exemplo)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configuração da sessão
app.secret_key = 'sua_chave_secreta_aqui'

# Funções para serializar e desserializar a sessão para/de cache
def get_session(sid):
    data = cache.get(sid)
    if data:
        return pickle.loads(data)
    return {}

def set_session(sid, data):
    cache.set(sid, pickle.dumps(data))

# Usar funções personalizadas para armazenar e recuperar sessão
app.session_interface.get_session = get_session
app.session_interface.set_session = set_session


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscreva_se')
def inscreva_se():
    return render_template('inscreva-se.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)