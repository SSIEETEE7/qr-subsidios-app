from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import qrcode
import os

app = Flask(__name__)

# Carpeta donde se guardan los QR
QR_FOLDER = os.path.join('static', 'qrs')
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route('/')
def index():
    qr_files = os.listdir(QR_FOLDER)
    return render_template('index.html', qr_files=qr_files)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    responsable = request.form['responsable']
    qr_data = f"Subsidio: 450 pesos - Responsable: {responsable}"
    qr = qrcode.make(qr_data)

    filename = f"{responsable}.png"
    path = os.path.join(QR_FOLDER, filename)
    qr.save(path)

    return redirect(url_for('index'))

@app.route('/static/qrs/<path:filename>')
def download_file(filename):
    return send_from_directory(QR_FOLDER, filename)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



