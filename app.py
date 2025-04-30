from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Simulación de productos por mercado
productos_por_mercado = {
    "Acocota": [
        {"nombre": "Manzana", "precio": 25, "imagen": "producto_manzana.jpg"},
        {"nombre": "Café", "precio": 80, "imagen": "producto_cafe.jpg"}
    ],
    "Emiliano Zapata": [
        {"nombre": "Tamal", "precio": 30, "imagen": "producto_tamal.jpg"},
        {"nombre": "Miel", "precio": 100, "imagen": "producto_miel.jpg"}
    ],
    "La Purísima": [
        {"nombre": "Frijol", "precio": 50, "imagen": "producto_frijol.jpg"}
    ]
}

# Mercados por municipio
mercados = {
    'Puebla Capital': ['Acocota', 'Emiliano Zapata'],
    'Tehuacán': ['Mercado La Purísima'],
    'San Martín Texmelucan': ['Mercado Benito Juárez', 'Domingo Arenas'],
    'Atlixco': ['Mercado Benito Juárez'],
    'Izúcar de Matamoros': ['Mercado Miguel Hidalgo', 'Mercado Municipal 5 de Mayo'],
    'Huauchinango': ['Mercado Municipal'],
    'Teziutlán': ['Mercado Victoria'],
    'Zacatlán': ['Mercado Revolución'],
    'Amozoc': ['Mercado Ignacio Zaragoza'],
    'Ajalpan': ['Mercado Municipal']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    productos = []
    for lista in productos_por_mercado.values():
        productos.extend(lista)
    return render_template('catalogo.html', productos=productos)

@app.route('/carrito')
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []
    total = sum(item['precio'] for item in session['carrito'])
    return render_template('carrito.html', carrito=session['carrito'], total=total)

@app.route('/agregar/<producto_nombre>')
def agregar_al_carrito(producto_nombre):
    for lista in productos_por_mercado.values():
        for producto in lista:
            if producto['nombre'] == producto_nombre:
                if 'carrito' not in session:
                    session['carrito'] = []
                session['carrito'].append(producto)
                session.modified = True
                break
    return redirect(url_for('catalogo'))

@app.route('/vaciar-carrito')
def vaciar_carrito():
    session['carrito'] = []
    session.modified = True
    return redirect(url_for('carrito'))

@app.route('/mercados', methods=['GET', 'POST'])
def mercados_view():
    seleccionados = {"municipio": None, "mercado": None}
    productos = []

    if request.method == 'POST':
        municipio = request.form.get('municipio')
        mercado = request.form.get('mercado')
        seleccionados["municipio"] = municipio
        seleccionados["mercado"] = mercado
        productos = productos_por_mercado.get(mercado, [])

    return render_template('mercados.html', mercados=mercados, seleccionados=seleccionados, productos=productos)

@app.route('/registro-locatarios', methods=['GET', 'POST'])
def registro_locatarios():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mercado = request.form['mercado']
        productos = request.form['productos']
        telefono = request.form['telefono']
        correo = request.form['correo']
        # Aquí podrías guardar en base de datos más adelante
        return render_template('registro-exitoso.html')
    return render_template('registro-locatarios.html')

@app.route('/admin-locatarios')
def admin_locatarios():
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
    print(app.url_map)


