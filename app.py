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
    'started_time': None,
    'started': None,
    'finish': None,
    'angle': 0,
    'current_angle':0,
    'current_count': 0,
    'once_time_sec':0,
    'move_count': 0,
    'latest_angle':180,
    'latest_time_h':2,
    'latest_time_m':0,
    'latest_move_count':2,
    'latest_mute': False,
}

@app.route('/')
def index():
    return render_template('index.html',
        max_rotation_speed=config['max_rotation_speed'],
        min_rotation_speed=config['min_rotation_speed'],
        latest_angle=device_state['latest_angle'],
        latest_move_count=device_state['latest_move_count'],
        latest_time_h=device_state['latest_time_h'],
        latest_time_m=device_state['latest_time_m'],
        latest_mute=device_state['latest_mute']
    )

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    angle = int(data['angle'])
    time_h = int(data['time_h'])
    time_m = int(data['time_m'])
    move_count = int(data['move_count'])
    mute = data['mute']  # mute の値を取得
    total_time_minutes = (time_h * 60 + time_m) * move_count
    total_angle = abs(angle) * move_count
    rotation_speed = total_angle / total_time_minutes if total_time_minutes > 0 else 0

    device_state['latest_angle'] = angle
    device_state['latest_time_h'] = time_h
    device_state['latest_time_m'] = time_m
    device_state['latest_move_count'] = move_count
    device_state['latest_mute'] = mute  # mute 値を latest_mute に記録

    if config['min_rotation_speed'] <= rotation_speed <= config['max_rotation_speed']:
        total_time = timedelta(hours=time_h, minutes=time_m) * move_count
        started_time = datetime.now()
        device_state.update({
            'status': 'running',
            'started_time': started_time,
            'started': started_time.strftime('%Y-%m-%d %H:%M:%S'),
            'finish': (started_time + total_time).strftime('%Y-%m-%d %H:%M:%S'),
            'angle': angle,
            'current_angle': 0,
            'current_count': 0,
            'once_time_sec': (time_h * 60 + time_m) + 60,
            'move_count': move_count
        })
        motor.motor_controller.run_start(angle, time_h, time_m, move_count, mute)  # モーター開始
    return '', 204

@app.route('/stop', methods=['POST'])
def stop():
    device_state['status'] = 'stopped'
    device_state['started_time'] = None
    motor.motor_controller.run_stop()  # モーター停止
    return '', 204

@app.route('/status')
def status():
    if device_state['started_time']:
        # モーターステータス取得から進捗更新
        is_running, current_angle, current_count = motor.motor_controller.get_run_status()
        device_state['current_angle'] = current_angle
        device_state['current_count'] = current_count
        if not is_running:
            device_state['status'] = 'stopped'

    return jsonify({
        'status': device_state['status'],
        'started': device_state['started'],
        'finish': device_state['finish'],
        'progress_angle': f"{device_state['current_angle']:.2f} / {abs(device_state['angle'])}",
        'progress_angle_percent': min((device_state['current_angle'] / abs(device_state['angle'])) * 100, 100),
        'progress_count': f"{device_state['current_count']} / {device_state['move_count']}",
        'progress_count_percent': min((device_state['current_count'] / device_state['move_count']) * 100, 100)
    })

@app.route('/move_start', methods=['POST'])
def move_start():
    data = request.get_json()
    speed = data['speed']  # 'fast' or 'slow'
    direction = data['direction']  # 'L' or 'R'
    mute = data['mute']
    motor.motor_controller.move_start(direction, speed, mute)  # 方向と速度を指定
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