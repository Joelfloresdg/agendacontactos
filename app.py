from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a base de datos
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Página principal (lista de contactos)
@app.route('/')
def index():
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

# Agregar nuevo contacto
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    conn = get_db_connection()
    conn.execute('INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)',
                 (name, email, phone))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Eliminar contacto
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
    
# Ver un contacto individual
@app.route('/view/<int:id>')
def view(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('view.html', contact=contact)
# Página para editar
@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', contact=contact)

# Guardar los cambios
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    conn = get_db_connection()
    conn.execute('UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?',
                 (name, email, phone, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3000)

