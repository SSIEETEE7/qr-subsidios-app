from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

# Lista de productos ejemplo
productos = [
    {'id': 1, 'nombre': 'Mole poblano', 'precio': 120},
    {'id': 2, 'nombre': 'Chile en nogada', 'precio': 150},
    {'id': 3, 'nombre': 'Tamal de dulce', 'precio': 25}
]

# Página principal
@app.route('/')
def home():
    return render_template('index.html')

# Catálogo de productos
@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', productos=productos)

# Mercados participantes
@app.route('/mercados')
def mercados():
    mercados_list = [
        {'nombre': 'Mercado de Sabores', 'descripcion': 'Antojitos poblanos.'},
        {'nombre': 'Mercado La Acocota', 'descripcion': 'Frutas y verduras.'},
        {'nombre': 'Mercado El Carmen', 'descripcion': 'Carnes y gastronomía típica.'}
    ]
    return render_template('mercados.html', mercados=mercados_list)

# Registro de locatarios
@app.route('/registro-locatarios', methods=['GET', 'POST'])
def registro_locatarios():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mercado = request.form['mercado']
        productos_loc = request.form['productos']
        telefono = request.form['telefono']
        correo = request.form['correo']

        # Guardar en base de datos
        conn = sqlite3.connect('subsidios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO locatarios (nombre, mercado, productos, telefono, correo)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, mercado, productos_loc, telefono, correo))
        conn.commit()
        conn.close()

        return render_template('registro-exitoso.html')
    return render_template('registro-locatarios.html')

# Confirmación de registro (vista)
@app.route('/confirmacion')
def confirmacion():
    return render_template('registro-exitoso.html')

# Página para usar QR (saldo)
@app.route('/usar-qr', methods=['GET', 'POST'])
def usar_qr():
    saldo = None
    mensaje = None
    codigo_qr = ""
    if request.method == 'POST':
        codigo_qr = request.form.get('codigo_qr', '')
        usar_saldo = request.form.get('usar_saldo')
        if usar_saldo:
            mensaje = '¡Compra realizada exitosamente con tu subsidio de $450 pesos!'
        else:
            saldo = 450  # saldo simulado
    return render_template('usar-qr.html', saldo=saldo, mensaje=mensaje, codigo_qr=codigo_qr)

# Admin de locatarios
@app.route('/admin-locatarios')
def admin_locatarios():
    conn = sqlite3.connect('subsidios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM locatarios')
    locatarios = cursor.fetchall()
    conn.close()
    return render_template('admin-locatarios.html', locatarios=locatarios)

# Carrito de compras
@app.route('/carrito')
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []
    carrito = session['carrito']
    total = sum(producto['precio'] for producto in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)

# Agregar producto al carrito
@app.route('/agregar/<int:producto_id>')
def agregar_al_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        session['carrito'].append(producto)
        session.modified = True
    
    return redirect(url_for('catalogo'))

# Vaciar carrito
@app.route('/vaciar-carrito')
def vaciar_carrito():
    session['carrito'] = []
    session.modified = True
    return redirect(url_for('carrito'))

# Iniciar app en local o Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
