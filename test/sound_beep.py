import json
import socket

# for sound
PORT_BEEP_SERVER = 54321
tone_base_do = 261.626
tone_base_re = 293.665
tone_base_mi = 329.628
tone_base_fa = 349.228
tone_base_so = 391.995
tone_base_ra = 440.000
tone_base_si = 493.883
tone_no  = 0   # no-sound
tone_sharp = 1.06
tone_do1 = int(tone_base_do * 1.0) # ド
tone_re1 = int(tone_base_re * 1.0) # レ
tone_mi1 = int(tone_base_mi * 1.0) # ミ
tone_fa1 = int(tone_base_fa * 1.0) # ファ
tone_so1 = int(tone_base_so * 1.0) # ソ
tone_ra1 = int(tone_base_ra * 1.0) # ラ
tone_si1 = int(tone_base_si * 1.0) # シ
tone_do2 = int(tone_base_do * 2.0) # ド
tone_re2 = int(tone_base_re * 2.0) # レ
tone_mi2 = int(tone_base_mi * 2.0) # ミ
tone_fa2 = int(tone_base_fa * 2.0) # ファ
tone_so2 = int(tone_base_so * 2.0) # ソ
tone_ra2 = int(tone_base_ra * 2.0) # ラ
tone_si2 = int(tone_base_si * 2.0) # シ
tone_do3 = int(tone_base_do * 3.0) # ド
tone_re3 = int(tone_base_re * 3.0) # レ
tone_mi3 = int(tone_base_mi * 3.0) # ミ
tone_fa3 = int(tone_base_fa * 3.0) # ファ
tone_so3 = int(tone_base_so * 3.0) # ソ
tone_ra3 = int(tone_base_ra * 3.0) # ラ
tone_si3 = int(tone_base_si * 3.0) # シ
tone_do4 = int(tone_base_do * 4.0) # ド

#音の長さ
len0 = 20
len1 = 200
len2 = 400
len3 = 600
len4 = 800

doremi_test= [
(tone_do1, len3),
(tone_re1, len3),
(tone_mi1, len3),
(tone_fa1, len3),
(tone_so1, len3),
(tone_ra1, len3),
(tone_si1, len3),
(tone_do2, len3),
(tone_re2, len3),
(tone_mi2, len3),
(tone_fa2, len3),
(tone_so2, len3),
(tone_ra2, len3),
(tone_si2, len3),
(tone_do3, len3),
(tone_re3, len3),
(tone_mi3, len3),
(tone_fa3, len3),
(tone_so3, len3),
(tone_ra3, len3),
(tone_si3, len3),
(tone_do4, len3),
]

spd_j = 1.0
jidai = [
(tone_do2*tone_sharp, len1/spd_j),#レb
(tone_re2*tone_sharp, len1/spd_j),#ミb
(tone_fa2, len3/spd_j),#ファー
(tone_fa2, len2/spd_j),#ファー
(tone_fa2, len1/spd_j),#ファ
(tone_fa2*tone_sharp, len3/spd_j),#ソbー
(tone_fa2, len1/spd_j),#ファ
(tone_re2*tone_sharp, len1/spd_j),#ミb
(tone_do2*tone_sharp, len1/spd_j),#レb
(tone_do2*tone_sharp, len3/spd_j),#レbー
(tone_do2, len1/spd_j),#ド
(tone_do2*tone_sharp, len1/spd_j),#レb
(tone_do2, len1/spd_j),#ド
(tone_ra1*tone_sharp, len3/spd_j),#シbー
(0, len1/spd_j),
(tone_ra1*tone_sharp, len1/spd_j),#シb
(tone_fa2*tone_sharp, len2/spd_j),#ソbー
(tone_fa2, len1/spd_j),#ファ
(tone_fa2*tone_sharp, len2/spd_j),#ソbー
(tone_fa2, len1/spd_j),#ファ
(tone_fa2*tone_sharp, len1/spd_j),#ソb
(tone_fa2, len1/spd_j),#ファ
(tone_re2*tone_sharp, len1/spd_j),#ミb
(tone_do2*tone_sharp, len1/spd_j),#レb
(tone_do2*tone_sharp, len1/spd_j),#レb
(tone_re2*tone_sharp, len1/spd_j),#ミb
(tone_fa2, len4/spd_j),#ファー
(tone_fa2*tone_sharp, len1/spd_j),#ソb
(tone_fa2, len1/spd_j),#ファ
(tone_re2*tone_sharp, len3/spd_j),#ミbー
(0, len1/spd_j),
(tone_fa2, len1/spd_j),#ファー
(tone_fa2*tone_sharp, len1/spd_j),#ソb
(tone_so2*tone_sharp, len3/spd_j),#ラbー
(tone_so2*tone_sharp, len2/spd_j),#ラbー
(tone_so2*tone_sharp, len1/spd_j),#ラb
(tone_ra2*tone_sharp, len3/spd_j),#シbー
(tone_fa2, len2/spd_j),#ファー
(tone_fa2, len1/spd_j),#ファ
(tone_so2*tone_sharp, len3/spd_j),#ラbー
(tone_so2*tone_sharp, len1/spd_j),#ラb
(tone_fa2*tone_sharp, len1/spd_j),#ソb
(tone_fa2, len1/spd_j),#ファ
(tone_so2*tone_sharp, len3/spd_j),#ラbー
(tone_fa2*tone_sharp, len3/spd_j),#ソbー
(0, len1/spd_j),
(tone_fa2, len1/spd_j),#ファ
(tone_fa2*tone_sharp, len1/spd_j),#ソb
(tone_so2*tone_sharp, len1/spd_j),#ラb
(tone_do2*tone_sharp, len1/spd_j),#レb
(tone_re2*tone_sharp, len1/spd_j),#ミb
(tone_fa2, len1/spd_j),#ファ
(tone_fa2*tone_sharp, len3/spd_j),#ソbー
(tone_fa2*tone_sharp, len1/spd_j),#ソb
(tone_fa2, len1/spd_j),#ファ
(tone_do2*tone_sharp, len1/spd_j),#ド
(tone_re2*tone_sharp, len3/spd_j),#ミbー
(tone_do2*tone_sharp, len4/spd_j),#レbー
]

mario_oneup = [
(tone_mi2, len1/2),
(tone_do3, len1/2),
(tone_mi3, len1/2),
(tone_do3, len1/2),
(tone_re3, len1/2),
(tone_so3, len1/2)
]

def play_sound_with_beep_server(sounds, delay):
    sock_info = ('127.0.0.1', PORT_BEEP_SERVER)
    data = { 'sounds': sounds, 'delay':delay }
    json_data = json.dumps(data).encode('utf-8')
    sock_fo_beep_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_fo_beep_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock_fo_beep_server.sendto(json_data, sock_info)


#play_sound_with_beep_server(mario_oneup, len0)
play_sound_with_beep_server(jidai, len0)
#play_sound_with_beep_server(doremi_test, len0)
