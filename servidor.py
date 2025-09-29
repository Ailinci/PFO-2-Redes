from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib

app = Flask(__name__)

# Creamos la base de datos, primero me fijo que no exista y luego la creo
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hasheado de contraseña
def hashear_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()

# Endpoint: Registro de usuarios
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contraseña = datos.get('contraseña')
    
    if not usuario or not contraseña:
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400
    
    contraseña_hash = hashear_contraseña(contraseña)
    
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)', 
                      (usuario, contraseña_hash))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El usuario ya existe'}), 400

# Endpoint: Login
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contraseña = datos.get('contraseña')
    
    if not usuario or not contraseña:
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400
    
    contraseña_hash = hashear_contraseña(contraseña)
    
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?', 
                  (usuario, contraseña_hash))
    usuario_encontrado = cursor.fetchone()
    conn.close()
    
    if usuario_encontrado:
        return jsonify({'mensaje': 'Login exitoso'}), 200
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

# Endpoint: Mostrar HTML de bienvenida
@app.route('/tareas', methods=['GET'])
def tareas():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bienvenida</title>
    </head>
    <body>
        <h1>Bienvenidos y bienvenidas al sistema</h1>
        <p>Pudiste ingresar correctamente</p>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)