CREATE TABLE IF NOT EXISTS locatarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    mercado TEXT NOT NULL,
    productos TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL
);
