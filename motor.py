import RPi.GPIO as GPIO
import threading
import time

import inspect
import sys
import sound

def debug_print(variable):
    # 呼び出し元のフレームを取得
    frame = inspect.currentframe().f_back
    # 変数名を検索
    for name, val in frame.f_locals.items():
        if val is variable:
            print(f"{name} : {variable}")
            return
    print(f"variable : {variable}")  # 名前が見つからない場合

# グローバルなMotorControllerインスタンス
motor_controller = None

def init(config):
    global motor_controller
    class MotorController:
        def __init__(self, config):
            self.pin_pul = 8
            self.pin_dir = 10
            self.pin_ena = 12
            self.config = config  # config.jsonをロードしたdict
            self.state = 'stopped'  # 状態遷移用: 'stopped', 'running(自動)', 'moving(手動)'
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin_pul, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.pin_dir, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.pin_ena, GPIO.OUT, initial=GPIO.LOW)
            self.thread_run = None
            self.thread_move = None
            self.is_running = False
            self.is_moving = False
            self.current_angle = 0
            self.current_count = 0
            sound.play_sound_with_beep_server(sound.mario_start)

        def run_start(self, angle, time_h, time_m, move_count, mute):
            if self.state == 'stopped':
                self.state = 'running'
                self.is_running = True
                self.current_angle = 0
                self.current_count = 0
                self.thread_run = threading.Thread(target=self._motor_thread_run, args=(angle, time_h, time_m, move_count, mute))
                self.thread_run.daemon = True
                self.thread_run.start()

        def run_stop(self):
            if self.state == 'running':
                self.state = 'stopped'
                self.is_running = False
                if self.thread_run:
                    self.thread_run.join(timeout=1)

        def get_run_status(self):
            return self.is_running, self.current_angle, self.current_count

        def _motor_thread_run(self, angle, time_h, time_m, move_count, mute):
            try:
                motor_driver_rate = float(self.config['motor_driver_rate'])
                gear_ratio = float(self.config['gear_ratio'])
                run_once_sec = (time_h * 60 + time_m) * 60
                if run_once_sec <= 0 or move_count <= 0 or angle == 0:
                    raise ValueError("time_h, time_m, move_count must be positive, angle must be non-zero")
                speed_deg_per_min = abs(angle) / (time_h * 60 + time_m)
                pulse_interval_sec = (360 * 60 / 200) / (speed_deg_per_min * gear_ratio * motor_driver_rate)
                pulse_width_sec = max(0.000005, min(0.1, pulse_interval_sec / 2))  # デューティ比50%、最小5μs、最大100ms
                pulses_per_move = int((abs(angle) * 200 * motor_driver_rate * gear_ratio) / 360)
            except (KeyError, ValueError) as e:
                print(f"設定エラー: {e}")
                return

            if not mute:
                sound.play_sound_with_beep_server(sound.yobikomikun)

            dir_level = GPIO.HIGH if angle < 0 else GPIO.LOW
            GPIO.output(self.pin_ena, GPIO.HIGH)
            GPIO.output(self.pin_dir, dir_level)

            started_time = time.perf_counter()
            next_time = started_time + pulse_interval_sec
            count_curr = 0
            pulse_count = 0
            while self.is_running and count_curr < move_count:
                GPIO.output(self.pin_pul, GPIO.HIGH)
                time.sleep(pulse_width_sec)
                GPIO.output(self.pin_pul, GPIO.LOW)
                time.sleep(max(0, next_time - time.perf_counter()))
                next_time += pulse_interval_sec
                pulse_count += 1
                # 方向更新
                if pulse_count >= pulses_per_move:
                    count_curr += 1
                    pulse_count = 0
                    GPIO.output(self.pin_dir, dir_level if count_curr % 2 == 0 else (GPIO.HIGH if dir_level == GPIO.LOW else GPIO.LOW))
                    if (not mute) and count_curr < move_count:
                        sound.play_sound_with_beep_server(sound.mario_oneup)
                # get status用
                self.current_angle = abs(angle) * pulse_count / pulses_per_move if count_curr < move_count else abs(angle)
                self.current_count = count_curr

            GPIO.output(self.pin_pul, GPIO.LOW)
            GPIO.output(self.pin_ena, GPIO.LOW)
            self.state = 'stopped'
            self.is_running = False
            if not mute:
                sound.play_sound_with_beep_server(sound.famima)

        def move_start(self, direction, speed, mute):
            """
            # direction: 'L'/'R'
            # speed:'fast'/'slow'
            """
            if self.state == 'stopped':
                self.state = 'moving'
                dir_level = GPIO.LOW if direction == 'L' else GPIO.HIGH
                speed_deg_per_min = self.config['move_rotation_speed_{}'.format(speed)]
                self.is_moving = True
                self.thread_move = threading.Thread(target=self._motor_thread_move, args=(dir_level, speed_deg_per_min, mute))
                self.thread_move.daemon = True
                self.thread_move.start()

        def move_stop(self):
            if self.state == 'moving':
                self.state = 'stopped'
                self.is_moving = False
                if self.thread_move:
                    self.thread_move.join(timeout=1)

        def _motor_thread_move(self, dir_level, speed_deg_per_min, mute):
            motor_driver_rate = self.config['motor_driver_rate']
            gear_ratio = self.config['gear_ratio']
            pulse_interval_sec = (360 * 60 / 200) / (speed_deg_per_min * gear_ratio * motor_driver_rate)
            pulse_width_sec = pulse_interval_sec / 2 #duty:50%
            debug_print(pulse_interval_sec)
            debug_print(pulse_width_sec)
            GPIO.output(self.pin_ena, GPIO.HIGH)
            GPIO.output(self.pin_dir, dir_level)

            sound_speed = 1.0
            if self.config['move_rotation_speed_fast'] == speed_deg_per_min:
                sound_speed = 1.3

            if not mute:
                if dir_level == GPIO.LOW:
                    sound.play_sound_with_beep_server(sound.tetorisu, sound.len0, sound_speed)
                else:
                    sound.play_sound_with_beep_server(sound.touryanse, sound.len0, sound_speed)

            next_time = time.perf_counter() + pulse_interval_sec
            while self.is_moving:
                GPIO.output(self.pin_pul, GPIO.HIGH)
                time.sleep(pulse_width_sec)
                GPIO.output(self.pin_pul, GPIO.LOW)
                time.sleep(max(0, next_time - time.perf_counter()))
                next_time += pulse_interval_sec

            GPIO.output(self.pin_pul, GPIO.LOW)
            GPIO.output(self.pin_ena, GPIO.LOW)

            if not mute:
                sound.play_sound_with_beep_server(sound.sound_stop)

        def cleanup(self):
            self.run_stop()
            GPIO.cleanup()

    motor_controller = MotorController(config)

# 初期化を明示的に呼び出すために必要
if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)
    init(config)
