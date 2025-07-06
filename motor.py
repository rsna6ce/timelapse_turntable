import RPi.GPIO as GPIO
import threading
import time

import inspect
import sys
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

        def run_start(self):
            if self.state == 'stopped' and self.config['min_rotation_speed'] <= 0 <= self.config['max_rotation_speed']:  # 簡単な検証
                self.state = 'running'
                self.is_running = True
                self.thread_run = threading.Thread(target=self._motor_thread_run)
                self.thread_run.daemon = True
                self.thread_run.start()
                GPIO.output(self.pin, GPIO.HIGH)

        def run_stop(self):
            if self.state in ['running', 'moving']:
                self.state = 'stopped'
                self.is_running = False
                if self.thread_run:
                    self.thread_run.join(timeout=1)
                GPIO.output(self.pin, GPIO.LOW)

        def _motor_thread_run(self):
            while self.is_running:
                time.sleep(0.1)  # 簡単なループ（実際は制御ロジック）

        def move_start(self, direction, speed):
            """
            # direction: 'L'/'R'
            # speed:'fast'/'slow'
            """
            if self.state == 'stopped':
                self.state = 'moving'
                # 方向と速度に応じた制御（仮実装）
                dir_level = GPIO.HIGH if direction == 'R' else GPIO.LOW
                speed_deg_per_min = self.config['move_rotation_speed_{}'.format(speed)]
                self.is_moving = True
                self.thread_move = threading.Thread(target=self._motor_thread_move, args=(dir_level, speed_deg_per_min))
                self.thread_move.daemon = True
                self.thread_move.start()

        def move_stop(self):
            if self.state == 'moving':
                self.state = 'stopped'
                self.is_moving = False
                if self.thread_move:
                    self.thread_move.join(timeout=1)

        def _motor_thread_move(self, dir_level, speed_deg_per_min):
            motor_driver_rate = self.config['motor_driver_rate']
            gear_ratio = self.config['gear_ratio']
            pulse_interval_sec = (360 * 60 / 200) / (speed_deg_per_min * gear_ratio * motor_driver_rate)
            pulse_width_sec = pulse_interval_sec / 2 #duty:50%
            debug_print(pulse_interval_sec)
            debug_print(pulse_width_sec)
            GPIO.output(self.pin_ena, GPIO.HIGH)
            GPIO.output(self.pin_dir, dir_level)

            next_time = time.perf_counter() + pulse_interval_sec
            while self.is_moving:
                GPIO.output(self.pin_pul, GPIO.HIGH)
                time.sleep(pulse_width_sec)
                GPIO.output(self.pin_pul, GPIO.LOW)
                time.sleep(max(0, next_time - time.perf_counter()))
                next_time += pulse_interval_sec

            GPIO.output(self.pin_pul, GPIO.LOW)
            GPIO.output(self.pin_ena, GPIO.LOW)

        def cleanup(self):
            self.stop()
            GPIO.cleanup()

    motor_controller = MotorController(config)

# 初期化を明示的に呼び出すために必要
if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)
    init(config)