from flask import Flask, jsonify, request, render_template
import sqlite3
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)

# Ruta principal para servir la página HTML
@app.route('/')
def index():
    return render_template('index.html')



# Ruta para obtener todos los gastos
@app.route('/gastos', methods=['GET'])
def obtener_gastos():
    # Conectar a la base de datos
    conexion = sqlite3.connect('gastos.db')
    cursor = conexion.cursor()
    # Obtener los gastos
    cursor.execute('SELECT * FROM gastos')
    gastos = cursor.fetchall()
    # Cerrar la conexión a la base de datos
    conexion.close()
    # Devolver los gastos en formato JSON
    return jsonify(gastos)

# Ruta para crear un nuevo gasto
@app.route('/gastos', methods=['POST'])
def crear_gasto():
    # Obtener los datos del gasto desde la petición POST
    concepto = request.json['concepto']
    monto = request.json['monto']
    fecha = request.json['fecha']
    # Conectar a la base de datos
    conexion = sqlite3.connect('gastos.db')
    cursor = conexion.cursor()
    # Insertar el nuevo gasto
    cursor.execute('INSERT INTO gastos (concepto, monto, fecha) VALUES (?, ?, ?)', (concepto, monto, fecha))
    conexion.commit()
    # Cerrar la conexión a la base de datos
    conexion.close()
    # Devolver una respuesta en formato JSON
    return jsonify({'message': 'El gasto ha sido creado correctamente'})

# Ruta para modificar un gasto existente
@app.route('/gastos/<int:id>', methods=['PUT'])
def modificar_gasto(id):
    # Obtener los datos del gasto desde la petición PUT
    concepto = request.json['concepto']
    monto = request.json['monto']
    fecha = request.json['fecha']
    # Conectar a la base de datos
    conexion = sqlite3.connect('gastos.db')
    cursor = conexion.cursor()
    # Actualizar el gasto
    cursor.execute('UPDATE gastos SET concepto=?, monto=?, fecha=? WHERE id=?', (concepto, monto, fecha, id))
    conexion.commit()
    # Cerrar la conexión a la base de datos
    conexion.close()
    # Devolver una respuesta en formato JSON
    return jsonify({'message': 'El gasto ha sido modificado correctamente'})

# Ruta para eliminar un gasto existente
@app.route('/gastos/<int:id>', methods=['DELETE'])
def eliminar_gasto(id):
    # Conectar a la base de datos
    conexion = sqlite3.connect('gastos.db')
    cursor = conexion.cursor()
    # Eliminar el gasto
    cursor.execute('DELETE FROM gastos WHERE id=?', (id,))
    conexion.commit()
    # Cerrar la conexión a la base de datos
    conexion.close()
    # Devolver una respuesta en formato JSON
    return jsonify({'message': 'El gasto ha sido eliminado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
