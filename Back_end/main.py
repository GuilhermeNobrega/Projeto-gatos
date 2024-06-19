from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['MYSQL_HOST'] = '10.88.80.3'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '|:rrNI%iLJ\F-ip3'
app.config['MYSQL_DB'] = 'petfind'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'petfind'

mysql = MySQL(app)

@app.route('/list/users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT idUser, email, userName, completeName, cep FROM User")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@app.route('/list/users/byid', methods=['POST'])
def get_users_by_id():
    if request.is_json:
        user = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT idUser, email, userName, completeName, pathUserImage, cep FROM User WHERE idUser = %s", (user['idUser']))
        userInfo = cursor.fetchall()
        cursor.close()
        if userInfo:
            # Transforma o resultado da consulta em um dicionário
            user_dict = {
                "idUser": userInfo[0],
                "email": userInfo[1],
                "userName": userInfo[2],
                "completeName": userInfo[3],
                "pathUserImage": userInfo[4],
                "cep": userInfo[5]
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT idUser, email, userName, completeName, cep FROM User")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT nome FROM Usuario WHERE id = %s", (user_id,))
#     user = cursor.fetchall()
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
        cursor.execute("SELECT userName, completeName, pathUserImage, email, cep FROM User WHERE (email = %s OR userName = %s) AND password = %s", (user['user'], user['user'], user['password']))
        userInfo = cursor.fetchall()
        cursor.close()
        if userInfo:
            # Transforma o resultado da consulta em um dicionário
            user_dict = {
                "userName": userInfo[0][0],
                "completeName": userInfo[0][1],
                "pathUserImage": userInfo[0][2],
                "email": userInfo[0][3],
                "cep": userInfo[0][4]
            }
            return jsonify({"msg": "Authenticated", "user": user_dict}), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify({"error": "Request must be JSON"}), 400


@app.route('/list/user_posts', methods=['POST'])
def list_user_posts():
    if request.is_json:
        vars = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Post WHERE fkIdUser = %s", (vars['userId']))
        posts = cursor.fetchall()
        cursor.close()
        if posts:
            return jsonify(posts), 200
        else:
            return jsonify({"msg": "No posts made by this user"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/list/all_posts', methods=['GET'])
def list_all_posts():
    post_list = []
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Post")
    postsRaw = cursor.fetchall()
    cursor.close()
    if postsRaw:
        for post in postsRaw:
            post_dict = {
                "id": post[0],
                "title": post[1],
                "description": post[2],
                "imagesPath": post[3],
                "postOwnerUserId": post[4],
                "localization": post[5],
                "publiType": post[6],
                "animalName": post[7],
                "animalSpecie": post[8],
                "animalGender": post[9],
                "animalColor": post[10],
                "animalSize": post[11],
                "postDate": post[12]
            }
            post_list.append(post_dict)
            
        return jsonify(post_list), 200
    else:
        return jsonify({"msg": "No posts to share with this user"}), 400

@app.route('/list/all_comments_from_post', methods=['POST'])
def list_all_comments_from_posts():
    if request.is_json:
        vars = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Comments WHERE fkIdPost = %s", (vars['fkIdPost']))
        posts = cursor.fetchall()
        cursor.close()
        if posts:
            return jsonify(posts), 200
        else:
            return jsonify({"msg": "No posts to share with this user"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

@app.route('/create/user', methods=['POST'])
def add_user():
    if request.is_json:
        vars = request.get_json()
        cursor = mysql.connection.cursor()
        # print(vars['cep'], vars['email'], vars['senha'], vars['nome'], vars['usuario'])
        cursor.execute("INSERT INTO User (cep, email, password, completeName, userName) VALUES (%s, %s, %s, %s, %s)", (vars['cep'], vars['email'], vars['password'], vars['completeName'], vars['userName']))
        mysql.connection.commit()
        cursor.close()
        return jsonify(vars['cep'], vars['email'], vars['password'], vars['completeName'], vars['userName']), 201
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)