import sqlite3
from flask import Flask, jsonify, request

app= Flask(__name__)

def crear_tabla():
    conection = sqlite3.connect("usuarios.db")
    cursor = conection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            name TEXT PRIMARY KEY,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL,
            CP TEXT NOT NULL
        )''')
    conection.commit()
    conection.close()

crear_tabla()

con = sqlite3.connect("usuarios.db")
cur = con.cursor()

try:
    cur.execute('''ALTER TABLE usuarios ADD COLUMN direccion TEXT NOT NULL DEFAULT AFTER telefono ''')
except:
    pass 

try:
    cur.execute('''ALTER TABLE usuarios ADD COLUMN CP TEXT NOT NULL AFTER direccion ''')
except:
    pass

con.commit()
con.close()

@app.route("/")
def root():
    return "home"

@app.route("/users/<user_name>")
def get_user(user_name):
    conection = sqlite3.connect("usuarios.db")
    cursor = conection.cursor()
    cursor.execute('''
        SELECT name, telefono, direccion, CP FROM usuarios
            WHERE name = ?
    ''', (user_name,))
    filas = cursor.fetchall()
    conection.close()

    if not filas:
        return jsonify({"error": "Usuario no encontrado"}), 404
    fila = filas[0]

    user = {'name': fila[0], 'telefono': fila[1], 'direccion': fila[2], 'CP':fila[3]}
    return jsonify(user), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/users", methods=['POST'])
def create_user():
    data = request.get_json()
    data["status"] = "user created"
    nombre = data.get("name")
    tlf = data.get("telefono")
    dir = data.get("direccion")
    codigo_postal = data.get("CP")

    conection = sqlite3.connect("usuarios.db")
    cursor = conection.cursor()
    cursor.execute('''
        INSERT INTO usuarios (name, telefono, direccion, CP) VALUES (?, ?, ?, ?)
    ''', (nombre, tlf, dir, codigo_postal))
    
    conection.commit()
    conection.close()
    
    return jsonify({"mensaje": "Usuario creado correctamente"}), 201

@app.route("/users", methods=['GET'])
def get__all_user():
    conection = sqlite3.connect("usuarios.db")
    cursor = conection.cursor()
    cursor.execute('''
        SELECT name, telefono, direccion, CP FROM usuarios
    ''')
    filas = cursor.fetchall()
    conection.close()

    if not filas:
        return jsonify({"mensaje": "No hay usuarios registrados"}), 200

    usuarios = []
    for fila in filas:
        usuarios.append({
            "name": fila[0],
            "telefono": fila[1],
            'direccion': fila[2],
            'CP':fila[3]
        })
    return jsonify(usuarios), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/users/<user_name>", methods=['DELETE'])
def delete_user(user_name):
    conection = sqlite3.connect("usuarios.db")
    cursor = conection.cursor()
    cursor.execute('''
        DELETE FROM usuarios
            WHERE name = ?
    ''', (user_name,))
    conection.commit()
    conection.close()

    return jsonify({"mensaje": f"Usuario con nombre {user_name} eliminado"}), 200

@app.route("/users/<user_name>", methods=['PUT'])
def update_user(user_name):
    data = request.get_json()
    nuevo_nombre = data.get("name")
    nuevo_tlf = data.get("telefono")
    nuevo_dir = data.get("direccion")
    nuevo_cp = data.get("CP")
    conection = sqlite3.connect("usuarios.db")
    cursor = conection.cursor()
    cursor.execute('''
        UPDATE usuarios
            SET name = ?, telefono = ?, direccion = ?, CP = ?
            WHERE name = ?
    ''', (nuevo_nombre, nuevo_tlf , nuevo_dir, nuevo_cp, user_name))
    conection.commit()
    
    return jsonify({"mensaje": f"Usuario con nombre {user_name} actualizado"}), 200

@app.route("/users", methods=["DELETE"])
def delete_all_users():
    con = sqlite3.connect("usuarios.db")
    cur = con.cursor()
    cur.execute("DELETE FROM usuarios")
    con.commit()
    con.close()
    return jsonify({"mensaje": "Todos los usuarios han sido eliminados"}), 200

if __name__ == "__main__":
    app.run(debug=True)