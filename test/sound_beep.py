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

spd_i=1.0
iphone = [
(tone_so1, len2/spd_i),#ソー
(tone_so1, len1/spd_i),#ソ
(tone_ra1*tone_sharp, len1/spd_i),#シb
(tone_do2, len1/spd_i),#ド
(tone_do2, len1/spd_i/2),#ド
(tone_ra1*tone_sharp, len1/spd_i/2),#シb
(tone_so1, len1/spd_i),#ソ
(tone_do2, len1/spd_i),#ド
(tone_fa1, len1/spd_i),#ファ
(tone_do2, len1/spd_i),#ド
(tone_ra1*tone_sharp, len1/spd_i),#シb
(tone_do2, len1/spd_i),#ド
(tone_fa1, len2/spd_i),#ファ
(0, len2/spd_i),
]
iphone.extend(iphone)

spt_t = 1.0
tetorisu = [
(tone_mi2, len2/spt_t),#ミー
(tone_si1, len1/spt_t),#シ
(tone_do2, len1/spt_t),#ド
(tone_re2, len2/spt_t),#レー
(tone_do2, len1/spt_t),#ド
(tone_si1, len1/spt_t),#シ
(tone_ra1, len2/spt_t),#ラー
(tone_ra1, len1/spt_t),#ラ
(tone_do2, len1/spt_t),#ド
(tone_mi2, len2/spt_t),#ミー
(tone_re2, len1/spt_t),#レ
(tone_do2, len1/spt_t),#ド
(tone_si1, len2/spt_t),#シー
(tone_si1, len1/spt_t),#シ
(tone_do2, len1/spt_t),#ド
(tone_re2, len2/spt_t),#レー
(tone_mi2, len2/spt_t),#ミー
(tone_do2, len2/spt_t),#ドー
(tone_ra1, len2/spt_t),#ラー
(tone_ra1, len3/spt_t),#ラー
(0, len1/spt_t),
(tone_re2, len2/spt_t),#レー
(tone_fa2, len1/spt_t),#ファ
(tone_ra2, len2/spt_t),#ラー
(tone_so2, len1/spt_t),#ソ
(tone_fa2, len1/spt_t),#ファ
(tone_mi2, len3/spt_t),#ミー
(tone_do2, len1/spt_t),#ド
(tone_mi2, len2/spt_t),#ミー
(tone_re2, len1/spt_t),#レ
(tone_do2, len1/spt_t),#ド
(tone_si1, len2/spt_t),#シー
(tone_si1, len1/spt_t),#シ
(tone_do2, len1/spt_t),#ド
(tone_re2, len2/spt_t),#レー
(tone_mi2, len2/spt_t),#ミー
(tone_do2, len2/spt_t),#ドー
(tone_ra1, len2/spt_t),#ラー
(tone_ra1, len2/spt_t),#ラー
]


spd_y = 1.0
yobikomikun = [
(tone_ra2, len1/spd_y),#ラ
(tone_ra2, len2/spd_y),#ラー
(tone_si2, len1/spd_y),#シ
(tone_ra2, len1/spd_y),#ラ
(tone_fa2*tone_sharp, len1/spd_y),#ファ#
(tone_ra2, len1/spd_y),#ラ
(0, len1/spd_y),
(tone_ra2, len1/spd_y),#ラ
(tone_ra2, len2/spd_y),#ラー
(tone_si2, len1/spd_y),#シ
(tone_ra2, len1/spd_y),#ラ
(tone_fa2*tone_sharp, len1/spd_y),#ファ#
(tone_ra2, len1/spd_y),#ラ
(0, len1/spd_y),
(tone_re2, len1/spd_y),#レ
(tone_re2, len1/spd_y),#レ
(tone_re2, len1/spd_y),#レ
(tone_mi2, len1/spd_y),#ミ
(tone_fa2*tone_sharp, len3/spd_y),#ファ#ー
(tone_re2, len1/spd_y),#レ
(tone_fa2*tone_sharp, len3/spd_y),#ファ#ー
(tone_ra2, len1/spd_y),##ラ
(tone_ra2, len3/spd_y),##ラー
(0, len1/spd_y),
(tone_re2, len1/spd_y),#レ
(tone_re2, len1/spd_y),#レ
(tone_re2, len1/spd_y),#レ
(tone_mi2, len1/spd_y),#ミ
(tone_fa2*tone_sharp, len4/spd_y),#ファ#ー
(0, len1/spd_y/16),
(tone_re2, len1/spd_y),#レ
(tone_re2, len1/spd_y),#レ
(tone_re2, len1/spd_y),#レ
(tone_mi2, len1/spd_y),#ミ
(tone_fa2*tone_sharp, len3/spd_y),#ファ#ー
(0, len1/spd_y),
(tone_mi2, len1/spd_y),#ミ
(tone_mi2, len1/spd_y),#ミ
(tone_mi2, len1/spd_y),#ミ
(tone_re2, len1/spd_y),#レ
(tone_mi2, len2/spd_y),#ミー
(tone_fa2*tone_sharp, len2/spd_y),#ファ#ー
(tone_ra2, len2/spd_y),#ラー
(tone_so2, len2/spd_y),#ソー
(tone_fa2*tone_sharp, len2/spd_y),#ファ#ー
(tone_mi2, len2/spd_y),#ミー
(0, len1/spd_y),
]
yobikomikun.extend(yobikomikun)



spd_f = 0.8
famima = [
(tone_so2, len1/spd_f),#ソ
(tone_re2*tone_sharp, len1/spd_f),#ミb
(tone_re1*tone_sharp, len1/spd_f),#シb
(tone_re2*tone_sharp, len1/spd_f),#ミb
(tone_fa2, len1/spd_f),#ファ
(tone_re3*tone_sharp, len3/spd_f),#シbー
(0, len1/spd_f/3),
(tone_fa1, len1/spd_f),#ファ
(tone_fa2, len1/spd_f),#ファ
(tone_so2, len1/spd_f),#ソ
(tone_fa2, len1/spd_f),#ファ
(tone_ra1*tone_sharp, len1/spd_f),#シb
(tone_re2*tone_sharp, len2/spd_f),#ミb
(0, len1/spd_f),
]
famima.extend(famima)

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
#play_sound_with_beep_server(jidai, len0)
#play_sound_with_beep_server(famima, len0)
play_sound_with_beep_server(yobikomikun, len0)
#play_sound_with_beep_server(tetorisu, len0)
#play_sound_with_beep_server(iphone, len0)
#play_sound_with_beep_server(doremi_test, len0)
