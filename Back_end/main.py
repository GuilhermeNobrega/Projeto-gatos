from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

@app.route('/users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT idUsuario, email, nome FROM Usuario")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT nome FROM Usuario WHERE id = %s", (user_id,))
#     user = cursor.fetchone()
#     cursor.close()
#     if user:
#         return jsonify(user)
#     else:
#         return jsonify({"error": "User not found"}), 404

@app.route('/validate_login', methods=['POST'])
def validate_login():
    if request.is_json:
        user = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT nome FROM Usuario WHERE (email = %s OR nome = %s) AND senha = %s", (user['user'], user['user'], user['password']))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return jsonify({"msg": "Authenticated"}), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify({"error": "Request must be JSON"}), 400


@app.route('/list_user_posts', methods=['POST'])
def list_user_posts():
    if request.is_json:
        vars = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT idPublicacao, local, especie, cor, raca, sexo, pelagem, porte, descricao FROM Publicacao WHERE usuarioIdFK = %s", (vars['userId']))
        posts = cursor.fetchone()
        cursor.close()
        if posts:
            return jsonify(posts), 200
        else:
            return jsonify({"msg": "No posts made by this user"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/list_all_posts', methods=['GET'])
def list_all_posts():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT idPublicacao, local, especie, cor, raca, sexo, pelagem, porte, descricao FROM Publicacao")
    posts = cursor.fetchone()
    cursor.close()
    if posts:
        return jsonify(posts), 200
    else:
        return jsonify({"msg": "No posts to share with this user"}), 400




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

@app.route('/user', methods=['POST'])
def add_user():
    if request.is_json:
        user = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, role) VALUES (%s, %s)", (user['name'], user['role']))
        mysql.connection.commit()
        cursor.close()
        return jsonify(user), 201
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True)