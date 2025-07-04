import RPi.GPIO as GPIO
import threading
from time import sleep

# グローバルなMotorControllerインスタンス
motor_controller = None

def init(config):
    global motor_controller
    class MotorController:
        def __init__(self, config):
            self.pin = 18
            self.config = config  # config.jsonをロードしたdict
            self.state = 'stopped'  # 状態遷移用: 'stopped', 'running', 'moving'
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            self.thread = None
            self.is_running = False

        def start(self):
            if self.state == 'stopped' and self.config['min_rotation_speed'] <= 0 <= self.config['max_rotation_speed']:  # 簡単な検証
                self.state = 'running'
                self.is_running = True
                self.thread = threading.Thread(target=self._run_motor)
                self.thread.daemon = True
                self.thread.start()
                GPIO.output(self.pin, GPIO.HIGH)

        def stop(self):
            if self.state in ['running', 'moving']:
                self.state = 'stopped'
                self.is_running = False
                if self.thread:
                    self.thread.join(timeout=1)
                GPIO.output(self.pin, GPIO.LOW)

        def move_start(self, direction, speed):
            if self.state == 'running':
                self.state = 'moving'
                # 方向と速度に応じた制御（仮実装）
                level = GPIO.HIGH if direction == 'R' else GPIO.LOW
                GPIO.output(self.pin, level)
                self._start_thread(speed)

        def move_stop(self):
            if self.state == 'moving':
                self.state = 'running'
                GPIO.output(self.pin, GPIO.LOW)
                if self.thread:
                    self.thread.join(timeout=1)

        def _run_motor(self):
            while self.is_running:
                sleep(0.1)  # 簡単なループ（実際は制御ロジック）

        def cleanup(self):
            self.stop()
            GPIO.cleanup()

    motor_controller = MotorController(config)

# 初期化を明示的に呼び出すために必要
if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)
    init(config)