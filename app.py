
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

productos = [
    {'id': 1, 'nombre': 'Café', 'precio': 80, 'imagen': 'producto_cafe.jpg'},
    {'id': 2, 'nombre': 'Manzana', 'precio': 25, 'imagen': 'producto_manzana.jpg'},
    {'id': 3, 'nombre': 'Miel', 'precio': 100, 'imagen': 'producto_miel.jpg'},
    {'id': 4, 'nombre': 'Tamal', 'precio': 30, 'imagen': 'producto_tamal.jpg'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', productos=productos)

@app.route('/carrito')
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []
    total = sum(item['precio'] for item in session['carrito'])
    return render_template('carrito.html', carrito=session['carrito'], total=total)

@app.route('/agregar/<int:producto_id>')
def agregar_al_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        session['carrito'].append(producto)
        session.modified = True
    return redirect(url_for('catalogo'))

@app.route('/vaciar-carrito')
def vaciar_carrito():
    session['carrito'] = []
    session.modified = True
    return redirect(url_for('carrito'))

@app.route('/mercados')
def mercados():
    mercados_data = [
        {'nombre': 'Mercado de Sabores', 'descripcion': 'Antojitos típicos poblanos.', 'imagen': 'foto_mapa_real.JPG'},
        {'nombre': 'Mercado La Acocota', 'descripcion': 'Frutas, verduras, y más.', 'imagen': 'hero_mercado.jpg'}
    ]
    return render_template('mercados.html', mercados=mercados_data)

@app.route('/registro-locatarios', methods=['GET', 'POST'])
def registro_locatarios():
    if request.method == 'POST':
        # Aquí iría la lógica de base de datos (comentada para Render)
        return render_template('registro-exitoso.html')
    return render_template('registro-locatarios.html')

@app.route('/admin-locatarios')
def admin_locatarios():
    # Locatarios simulados (sin BD)
    locatarios = [
        ('Juan Pérez', 'Acocota', 'Frutas', '2221234567', 'juan@example.com'),
        ('Ana Ruiz', 'Sabores', 'Antojitos', '2227654321', 'ana@example.com')
    ]
    return render_template('admin-locatarios.html', locatarios=locatarios)

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

if __name__ == '__main__':
    app.run(debug=True)
