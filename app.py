from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, timedelta
import motor

app = Flask(__name__)

# config.json から設定を読み込む
with open('config.json', 'r') as f:
    config = json.load(f)

# MotorControllerに設定を渡して初期化
motor.init(config)

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
    return render_template('index.html', max_rotation_speed=config['max_rotation_speed'], min_rotation_speed=config['min_rotation_speed'])

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    angle = int(data['angle'])
    time_h = int(data['time_h'])
    time_m = int(data['time_m'])
    move_count = int(data['move_count'])
    total_time_minutes = (time_h * 60 + time_m) * move_count
    total_angle = abs(angle) * move_count
    rotation_speed = total_angle / total_time_minutes if total_time_minutes > 0 else 0

    if config['min_rotation_speed'] <= rotation_speed <= config['max_rotation_speed']:
        total_time = timedelta(hours=time_h, minutes=time_m) * move_count
        device_state.update({
            'status': 'running',
            'started': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'finish': (datetime.now() + total_time).strftime('%Y-%m-%d %H:%M:%S'),
            'angle': angle,
            'count': 0,
            'total_angle': total_angle,
            'move_count': move_count
        })
        motor.motor_controller.start()  # モーター開始
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
    motor.motor_controller.stop()  # モーター停止
    return '', 204

@app.route('/status')
def status():
    if device_state['status'] == 'running':
        progress_angle = (device_state['count'] * abs(device_state['angle']))
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
    speed = data['speed']  # 'fast' or 'slow'
    direction = data['direction']  # 'L' or 'R'
    motor.motor_controller.move_start(direction, speed)  # 方向と速度を指定
    return '', 204

@app.route('/move_stop', methods=['POST'])
def move_stop():
    motor.motor_controller.move_stop()
    return '', 204

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        motor.motor_controller.cleanup()