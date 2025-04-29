from flask import Flask, render_template, request, redirect, url_for

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

@app.route('/usar-qr', methods=['GET', 'POST'])
def usar_qr():
    saldo = None
    if request.method == 'POST':
        codigo_qr = request.form['codigo_qr']
        # Aquí más adelante validaremos que el QR sea válido
        saldo = 450  # Simulamos saldo fijo
    return render_template('usar-qr.html', saldo=saldo)

@app.route('/registro-locatarios', methods=['GET', 'POST'])
def registro_locatarios():
    if request.method == 'POST':
        # Aquí puedes capturar los datos enviados
        nombre = request.form['nombre']
        mercado = request.form['mercado']
        productos = request.form['productos']
        telefono = request.form['telefono']
        correo = request.form['correo']
        # Aquí luego podemos guardar esos datos en una base de datos
        print(f"Registro recibido: {nombre}, {mercado}, {productos}, {telefono}, {correo}")
        return redirect(url_for('home'))  # Después de registrar, regresa al inicio
    return render_template('registro-locatarios.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
