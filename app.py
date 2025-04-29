from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/mercados')
def mercados():
    return render_template('mercados.html')

@app.route('/registro-locatarios', methods=['GET', 'POST'])
def registro_locatarios():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mercado = request.form['mercado']
        productos = request.form['productos']
        telefono = request.form['telefono']
        correo = request.form['correo']
        conn = sqlite3.connect('subsidios.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO locatarios (nombre, mercado, productos, telefono, correo)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, mercado, productos, telefono, correo))
        conn.commit()
        conn.close()
        return render_template('registro-exitoso.html')
    return render_template('registro-locatarios.html')

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
            saldo = 450
    return render_template('usar-qr.html', saldo=saldo, mensaje=mensaje, codigo_qr=codigo_qr)

@app.route('/admin-locatarios')
def admin_locatarios():
    conn = sqlite3.connect('subsidios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM locatarios')
    locatarios = cursor.fetchall()
    conn.close()
    return render_template('admin-locatarios.html', locatarios=locatarios)

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
