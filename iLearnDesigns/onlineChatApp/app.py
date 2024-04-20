# pip install flask flask-socketio
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.secret_key = 'your secret key'
socketio = SocketIO(app)

# Users and their rooms info
users = {}
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    session['username'] = username
    users[username] = {"friends": []}
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('home.html', username=session['username'])

@app.route('/create_room', methods=['POST'])
def create_room():
    username = session['username']
    roomname = request.form.get('roomname')
    rooms[roomname] = {"participants": [username]}
    return redirect(url_for('chat', roomname=roomname))

@app.route('/join_room/<roomname>')
def join_room(roomname):
    username = session['username']
    rooms[roomname]['participants'].append(username)
    return render_template('chat.html', roomname=roomname)

@app.route('/leave_room/<roomname>')
def leave_room(roomname):
    username = session['username']
    rooms[roomname]['participants'].remove(username)
    return redirect(url_for('home'))

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'], data['room'], data['message']))
    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)