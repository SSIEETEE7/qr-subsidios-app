from flask import Flask, render_template, request
import qrcode
import base64
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        img = qrcode.make(f'Subsidio para: {nombre}')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return render_template('index.html', qr_image=qr_image)

if __name__ == '__main__':
    app.run(debug=True)
