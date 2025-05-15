from flask_socketio import render_template, emit, join_room, leave_room
from Website import create_app

app = create_app()

if __name__ == '__main__':
    app.run()