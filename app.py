from flask import Flask, render_template, request, redirect, url_for, session
import os
import uuid
import qrcode

app = Flask(__name__)
app.secret_key = 'clave_secreta'

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

# Productos simulados por mercado
productos_por_mercado = {
    "Acocota": [
        {"nombre": "Manzana", "precio": 25, "imagen": "producto_manzana.jpg"},
        {"nombre": "Café", "precio": 80, "imagen": "producto_cafe.jpg"}
    ],
    "Emiliano Zapata": [
        {"nombre": "Tamal", "precio": 30, "imagen": "producto_tamal.jpg"},
        {"nombre": "Miel", "precio": 100, "imagen": "producto_miel.jpg"}
    ]
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', mercados=mercados)

@app.route('/catalogo')
def catalogo():
    productos = []
    for lista in productos_por_mercado.values():
        productos.extend(lista)
    return render_template('catalogo.html', productos=productos)

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

@app.route('/carrito')
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []
    total = sum(item['precio'] for item in session['carrito'])
    return render_template('carrito.html', carrito=session['carrito'], total=total)

@app.route('/vaciar-carrito')
def vaciar_carrito():
    session['carrito'] = []
    session.modified = True
    return redirect(url_for('carrito'))

@app.route('/registro-locatarios', methods=['GET', 'POST'])
def registro_locatarios():
    if request.method == 'POST':
        return render_template('registro-exitoso.html')
    return render_template('registro-locatarios.html')

@app.route('/admin-locatarios')
def admin_locatarios():
    locatarios = [
        ('Juan Pérez', 'Acocota', 'Frutas', '2221234567', 'juan@example.com'),
        ('Ana Ruiz', 'Sabores', 'Antojitos', '2227654321', 'ana@example.com')
    ]
    return render_template('admin-locatarios.html', locatarios=locatarios)

@app.route('/usar-qr')
def usar_qr():
    qr_dir = os.path.join('static', 'img', 'qr')
    os.makedirs(qr_dir, exist_ok=True)

    codigo = str(uuid.uuid4())
    valor = 450
    contenido = f"QR-{codigo}-MXN{valor}"
    nombre_archivo = f"{codigo}.png"
    ruta_archivo = os.path.join(qr_dir, nombre_archivo)

    qr_img = qrcode.make(contenido)
    qr_img.save(ruta_archivo)

    return render_template('usar-qr.html', qr_file=nombre_archivo, qr_content=contenido)

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


@app.route('/qr/<nombre>')
def qr_personal(nombre):
    nombre = nombre.lower()
    saldos = {
        'erik': 450,
        'victor': 200
    }
    saldo = saldos.get(nombre)
    if saldo is None:
        return "QR no válido o beneficiario no encontrado", 404

    return render_template('qr-personal.html', nombre=nombre.capitalize(), saldo=saldo)


if __name__ == '__main__':
    app.run(debug=True)
