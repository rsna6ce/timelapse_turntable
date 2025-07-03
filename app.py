from flask import Flask, render_template, request, jsonify
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Simulated device state
device_state = {
    'status': 'stopped',
    'started': None,
    'finish': None,
    'angle': 0,
    'count': 0,
    'total_angle': 0,
    'move_count': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    angle = int(data['angle'])
    time_h = int(data['time_h'])
    time_m = int(data['time_m'])
    move_count = int(data['move_count'])
    total_time = timedelta(hours=time_h, minutes=time_m) * move_count
    device_state.update({
        'status': 'running',
        'started': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'finish': (datetime.now() + total_time).strftime('%Y-%m-%d %H:%M:%S'),
        'angle': angle,
        'count': 0,
        'total_angle': angle * move_count,
        'move_count': move_count
    })
    return '', 204

@app.route('/stop', methods=['POST'])
def stop():
    device_state.update({
        'status': 'stopped',
        'started': None,
        'finish': None,
        'angle': 0,
        'count': 0,
        'total_angle': 0,
        'move_count': 0
    })
    return '', 204

@app.route('/status')
def status():
    if device_state['status'] == 'running':
        progress_angle = (device_state['count'] * device_state['angle'])
        progress_count = (device_state['count'] / device_state['move_count']) * 100
        return jsonify({
            'status': 'running',
            'started': device_state['started'],
            'finish': device_state['finish'],
            'progress_angle': f"{progress_angle} / {device_state['total_angle']}",
            'progress_angle_percent': min((progress_angle / device_state['total_angle']) * 100, 100),
            'progress_count': f"{device_state['count']} / {device_state['move_count']}",
            'progress_count_percent': min(progress_count, 100)
        })
    return jsonify({'status': 'stopped'})

@app.route('/move_start', methods=['POST'])
def move_start():
    data = request.get_json()
    # Simulate move start (implement actual device control here)
    return '', 204

@app.route('/move_stop', methods=['POST'])
def move_stop():
    # Simulate move stop (implement actual device control here)
    return '', 204

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
