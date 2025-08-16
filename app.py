from flask import Flask, render_template, jsonify
import voice_control
import gesture_mock
import threading
import os
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

# Shared state
app_state = {
    'voice_active': False,
    'last_command': None,
    'last_response': None
}

@app.route('/')
def index():
    return render_template('index.html', 
                         voice_active=app_state['voice_active'],
                         last_command=app_state['last_command'],
                         last_response=app_state['last_response'])

@app.route('/voice_status')
def voice_status():
    return jsonify({
        'active': app_state['voice_active'],
        'last_command': app_state['last_command'],
        'last_response': app_state['last_response']
    })

def update_state(key, value):
    app_state[key] = value
    socketio.emit('state_update', {'key': key, 'value': value})

def start_voice_assistant():
    """Start the voice assistant with state updates"""
    try:
        update_state('voice_active', True)
        voice_control.initialize_voice_assistant(
            command_callback=lambda cmd: update_state('last_command', cmd),
            response_callback=lambda res: update_state('last_response', res)
        )
    finally:
        update_state('voice_active', False)

def start_gesture_control():
    """Start gesture control"""
    gesture_mock.start_gesture_control()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Start services in threads
    voice_thread = threading.Thread(target=start_voice_assistant)
    voice_thread.daemon = True
    voice_thread.start()
    
    gesture_thread = threading.Thread(target=start_gesture_control)
    gesture_thread.daemon = True
    gesture_thread.start()
    
    print(f"\n🚀 MAINEC App is running at http://localhost:{port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True)