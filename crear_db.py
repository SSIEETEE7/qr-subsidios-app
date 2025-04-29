import sqlite3

# Conectar o crear la base de datos
conn = sqlite3.connect('subsidios.db')
cursor = conn.cursor()

# Crear la tabla locatarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS locatarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    mercado TEXT NOT NULL,
    productos TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Base de datos 'subsidios.db' creada con éxito ✅")
