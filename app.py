from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app)

DATABASE = 'database.db'


def init_db():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def index():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT username, message FROM posts ORDER BY id DESC')

    posts = cursor.fetchall()

    conn.close()

    return render_template('index.html', posts=posts)


@app.route('/post', methods=['POST'])
def post():

    username = request.form['user']
    message = request.form['message']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO posts (username, message) VALUES (?, ?)',
        (username, message)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@socketio.on('message')
def handle_message(msg):
    print('Mensaje:', msg)
    send(msg, broadcast=True)


if __name__ == '__main__':

    init_db()

    socketio.run(app, debug=True)