#!/usr/bin/env python3
import sys
import time
import socket
import json
import threading
import queue
import wiringpi

OUTPIN = 13
PORT = 54321
PWM_RANGE = 20

q = queue.Queue()

def play_melody_thread():
    while True:
        data = q.get()
        sounds = data['sounds']
        delay = data['delay']
        speed = data['speed']
        for sound in sounds:
            if not q.empty():
                #cancel and play next sound
                break
            freq = sound[0]
            time_ms = sound[1]
            if freq:
                # raspi3 baseClock = 19.2*10**6
                # f(Hz) = baseClock / pwmClock / pwmRange
                # pwmClock = baseClock / pwmRange / f
                clock = int(19.2*10**6 / PWM_RANGE / freq)
                #print("clock", clock)
                wiringpi.pwmSetClock(clock)
                wiringpi.pwmWrite(OUTPIN, int(PWM_RANGE/2))
            else:
                # no-sound silence
                wiringpi.pwmWrite(OUTPIN,0)
            time.sleep(time_ms/speed/(1000))
            wiringpi.pwmWrite(OUTPIN,0)
            time.sleep(delay/speed/1000)

def main():
    #init device
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(OUTPIN, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pwmSetMode(wiringpi.PWM_MODE_MS)
    wiringpi.pwmSetRange(PWM_RANGE)

    #init thread
    th = threading.Thread(target=play_melody_thread, name='play_melody_thread',daemon=True)
    th.start()

    #init udp
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', PORT))
    while True:
        json_data, addr = sock.recvfrom(4096)
        try:
            data = json.loads(json_data.decode('utf-8'))
            sounds = data.get('sounds',[(0,0)])
            delay = data.get('delay',20)
            speed = data.get('speed',1.0)
            q.put({'sounds':sounds, 'delay':delay, 'speed':speed})
        except:
            # ignore do nothing
            pass

if __name__ == '__main__':
    sys.exit(main())