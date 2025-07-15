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

# 音の停止
sound_stop=[(0,len0)]

spd_touryanse=1.0
touryanse=[
(tone_mi2, len2/spd_touryanse),#ミー
(tone_mi2, len2/spd_touryanse),#ミー
(tone_re2, len2/spd_touryanse),#レー
(tone_mi2, len2/spd_touryanse),#ミー
(tone_mi2, len1/spd_touryanse),#ミ
(tone_re2, len1/spd_touryanse),#レ
(tone_si1, len2/spd_touryanse),#シー
(0, len1),
(tone_fa2, len2/spd_touryanse),#ファー
(tone_fa2, len1/spd_touryanse),#ファ
(tone_fa2, len1/spd_touryanse),#ファ
(tone_ra2, len2/spd_touryanse),#ラー
(tone_fa2, len1/spd_touryanse),#ファ
(tone_mi2, len1/spd_touryanse),#ミ
(tone_fa2, len1/spd_touryanse),#ファ
(tone_mi2, len1/spd_touryanse),#ミ
(tone_re2, len1/spd_touryanse),#レ
(tone_re2, len1/spd_touryanse),#レ
(tone_mi2, len2/spd_touryanse),#ミー
(0, len1),
(tone_fa2, len2/spd_touryanse),#ファー
(tone_fa2, len2/spd_touryanse),#ファー
(0, len1/2),
(tone_ra2, len1/spd_touryanse),#ラ
(tone_fa2, len1/spd_touryanse),#ファ
(tone_mi2, len1/spd_touryanse),#ミ
(tone_fa2, len1/spd_touryanse),#ファ
(tone_mi2, len1/spd_touryanse),#ミ
(tone_re2, len1/spd_touryanse),#レ
(tone_re2, len1/spd_touryanse),#レ
(tone_mi2, len2/spd_touryanse),#ミー
(0, len1),
(tone_do2, len2/spd_touryanse),#ドー
(tone_do2, len1/spd_touryanse),#ド
(tone_do2, len1/spd_touryanse),#ド
(tone_mi2, len2/spd_touryanse),#ミー
(tone_do2, len1/spd_touryanse),#ド
(tone_si1, len1/spd_touryanse),#シ
(tone_do2, len1/spd_touryanse),#ド
(tone_si1, len1/spd_touryanse),#シ
(tone_ra1, len1/spd_touryanse),#ラ
(tone_ra1, len1/spd_touryanse),#ラ
(tone_si1, len2/spd_touryanse),#シー
(0, len1),
(tone_do2, len1/spd_touryanse),#ド
(tone_do2, len2/spd_touryanse),#ドー
(tone_do2, len1/spd_touryanse),#ド
(tone_mi2, len1/spd_touryanse),#ミ
(tone_mi2, len1/spd_touryanse),#ミ
(tone_do2, len1/spd_touryanse),#ド
(tone_si1, len1/spd_touryanse),#シ
(tone_do2, len1/spd_touryanse),#ド
(tone_si1, len1/spd_touryanse),#シ
(tone_ra1, len1/spd_touryanse),#ラ
(tone_ra1, len1/spd_touryanse),#ラ
(tone_si1, len2/spd_touryanse),#シー

(tone_si2, len2/spd_touryanse),#シー
(tone_fa2, len2/spd_touryanse),#ファー
(tone_si2, len2/spd_touryanse),#シー
(tone_fa2, len2/spd_touryanse),#ファー
(tone_si2, len2/spd_touryanse),#シー
(tone_fa2, len2/spd_touryanse),#ファー
(tone_si2, len2/spd_touryanse),#シー
(tone_fa2, len2/spd_touryanse),#ファー
(0, len1),
]

# スモールワールド
spd_small_world=1.2
small_world = [
(tone_si1, len1/spd_small_world),#シ
(tone_do1, len1/spd_small_world),#ド
(tone_re2, len2/spd_small_world),#レー
(tone_si2, len2/spd_small_world),#シー
(tone_so2, len2/spd_small_world),#ソー
(tone_ra2, len1/spd_small_world),#ラ
(tone_so2, len1/spd_small_world),#ソ
(tone_so2, len2/spd_small_world),#ソー
(tone_fa2*tone_sharp, len2/spd_small_world),#ファー#
(tone_fa2*tone_sharp, len2/spd_small_world),#ファー#
(0, len1/spd_small_world),
(tone_ra1, len1/spd_small_world),#ラ
(tone_si1, len1/spd_small_world),#シ
(tone_do2, len2/spd_small_world),#ドー
(tone_ra2, len2/spd_small_world),#ラー
(tone_fa2*tone_sharp, len2/spd_small_world),#ファー#
(tone_so2, len1/spd_small_world),#ソ
(tone_fa2*tone_sharp, len1/spd_small_world),#ファ#
(tone_mi2, len2/spd_small_world),#ミー
(tone_re2, len2/spd_small_world),#レー
(tone_re2, len2/spd_small_world),#レー
(0, len1/spd_small_world),
(tone_si1, len1/spd_small_world),#シ
(tone_do1, len1/spd_small_world),#ド
(tone_re2, len2/spd_small_world),#レー
(tone_so2, len1/spd_small_world),#ソ
(tone_ra2, len1/spd_small_world),#ラ
(tone_si2, len2/spd_small_world),#シー
(tone_ra2, len1/spd_small_world),#ラ
(tone_so2, len1/spd_small_world),#ソ
(tone_mi2, len2/spd_small_world),#ミー
(tone_ra2, len1/spd_small_world),#ラ
(tone_si2, len1/spd_small_world),#シ
(tone_do3, len1/spd_small_world),#ド
(tone_si2, len1/spd_small_world),#シ
(tone_ra2, len1/spd_small_world),#ラ
(tone_re2, len2/spd_small_world),#レー
(tone_do3, len2/spd_small_world),#ドー
(tone_si2, len2/spd_small_world),#シー
(tone_ra2, len2/spd_small_world),#ラー
(tone_so2, len2/spd_small_world),#ソー
(0, len1/spd_small_world),
]
small_world.extend(small_world)

# iphone着信
spd_iphone=1.2
iphone = [
(tone_so1, len2/spd_iphone),#ソー
(tone_so1, len1/spd_iphone),#ソ
(tone_ra1*tone_sharp, len1/spd_iphone),#シb
(tone_do2, len1/spd_iphone),#ド
(tone_do2, len1/spd_iphone/2),#ド
(tone_ra1*tone_sharp, len1/spd_iphone/2),#シb
(tone_so1, len1/spd_iphone),#ソ
(tone_do2, len1/spd_iphone),#ド
(tone_fa1, len1/spd_iphone),#ファ
(tone_do2, len1/spd_iphone),#ド
(tone_ra1*tone_sharp, len1/spd_iphone),#シb
(tone_do2, len1/spd_iphone),#ド
(tone_fa1, len2/spd_iphone),#ファ
(0, len2/spd_iphone),
]

# テトリス
spd_tetorisu = 1.0
tetorisu = [
(tone_mi2, len2/spd_tetorisu),#ミー
(tone_si1, len1/spd_tetorisu),#シ
(tone_do2, len1/spd_tetorisu),#ド
(tone_re2, len2/spd_tetorisu),#レー
(tone_do2, len1/spd_tetorisu),#ド
(tone_si1, len1/spd_tetorisu),#シ
(tone_ra1, len2/spd_tetorisu),#ラー
(tone_ra1, len1/spd_tetorisu),#ラ
(tone_do2, len1/spd_tetorisu),#ド
(tone_mi2, len2/spd_tetorisu),#ミー
(tone_re2, len1/spd_tetorisu),#レ
(tone_do2, len1/spd_tetorisu),#ド
(tone_si1, len2/spd_tetorisu),#シー
(tone_si1, len1/spd_tetorisu),#シ
(tone_do2, len1/spd_tetorisu),#ド
(tone_re2, len2/spd_tetorisu),#レー
(tone_mi2, len2/spd_tetorisu),#ミー
(tone_do2, len2/spd_tetorisu),#ドー
(tone_ra1, len2/spd_tetorisu),#ラー
(tone_ra1, len3/spd_tetorisu),#ラー
(0, len1/spd_tetorisu),
(tone_re2, len2/spd_tetorisu),#レー
(tone_fa2, len1/spd_tetorisu),#ファ
(tone_ra2, len2/spd_tetorisu),#ラー
(tone_so2, len1/spd_tetorisu),#ソ
(tone_fa2, len1/spd_tetorisu),#ファ
(tone_mi2, len3/spd_tetorisu),#ミー
(tone_do2, len1/spd_tetorisu),#ド
(tone_mi2, len2/spd_tetorisu),#ミー
(tone_re2, len1/spd_tetorisu),#レ
(tone_do2, len1/spd_tetorisu),#ド
(tone_si1, len2/spd_tetorisu),#シー
(tone_si1, len1/spd_tetorisu),#シ
(tone_do2, len1/spd_tetorisu),#ド
(tone_re2, len2/spd_tetorisu),#レー
(tone_mi2, len2/spd_tetorisu),#ミー
(tone_do2, len2/spd_tetorisu),#ドー
(tone_ra1, len2/spd_tetorisu),#ラー
(tone_ra1, len2/spd_tetorisu),#ラー
]
tetorisu.extend(tetorisu)


# 呼び込み君
sdp_yobi = 1.0
yobikomikun = [
(tone_ra2, len1/sdp_yobi),#ラ
(tone_ra2, len2/sdp_yobi),#ラー
(tone_si2, len1/sdp_yobi),#シ
(tone_ra2, len1/sdp_yobi),#ラ
(tone_fa2*tone_sharp, len1/sdp_yobi),#ファ#
(tone_ra2, len1/sdp_yobi),#ラ
(0, len1/sdp_yobi),
(tone_ra2, len1/sdp_yobi),#ラ
(tone_ra2, len2/sdp_yobi),#ラー
(tone_si2, len1/sdp_yobi),#シ
(tone_ra2, len1/sdp_yobi),#ラ
(tone_fa2*tone_sharp, len1/sdp_yobi),#ファ#
(tone_ra2, len1/sdp_yobi),#ラ
(0, len1/sdp_yobi),
(tone_re2, len1/sdp_yobi),#レ
(tone_re2, len1/sdp_yobi),#レ
(tone_re2, len1/sdp_yobi),#レ
(tone_mi2, len1/sdp_yobi),#ミ
(tone_fa2*tone_sharp, len3/sdp_yobi),#ファ#ー
(tone_re2, len1/sdp_yobi),#レ
(tone_fa2*tone_sharp, len3/sdp_yobi),#ファ#ー
(tone_ra2, len1/sdp_yobi),##ラ
(tone_ra2, len3/sdp_yobi),##ラー
(0, len1/sdp_yobi),
(tone_re2, len1/sdp_yobi),#レ
(tone_re2, len1/sdp_yobi),#レ
(tone_re2, len1/sdp_yobi),#レ
(tone_mi2, len1/sdp_yobi),#ミ
(tone_fa2*tone_sharp, len4/sdp_yobi),#ファ#ー
(0, len1/sdp_yobi/16),
(tone_re2, len1/sdp_yobi),#レ
(tone_re2, len1/sdp_yobi),#レ
(tone_re2, len1/sdp_yobi),#レ
(tone_mi2, len1/sdp_yobi),#ミ
(tone_fa2*tone_sharp, len3/sdp_yobi),#ファ#ー
(0, len1/sdp_yobi),
(tone_mi2, len1/sdp_yobi),#ミ
(tone_mi2, len1/sdp_yobi),#ミ
(tone_mi2, len1/sdp_yobi),#ミ
(tone_re2, len1/sdp_yobi),#レ
(tone_mi2, len2/sdp_yobi),#ミー
(tone_fa2*tone_sharp, len2/sdp_yobi),#ファ#ー
(tone_ra2, len2/sdp_yobi),#ラー
(tone_so2, len2/sdp_yobi),#ソー
(tone_fa2*tone_sharp, len2/sdp_yobi),#ファ#ー
(tone_mi2, len2/sdp_yobi),#ミー
(0, len1/sdp_yobi),
]
yobikomikun.extend(yobikomikun)

# ファミマ入店
spd_famima = 0.8
famima = [
(tone_so2, len1/spd_famima),#ソ
(tone_re2*tone_sharp, len1/spd_famima),#ミb
(tone_re1*tone_sharp, len1/spd_famima),#シb
(tone_re2*tone_sharp, len1/spd_famima),#ミb
(tone_fa2, len1/spd_famima),#ファ
(tone_re3*tone_sharp, len3/spd_famima),#シbー
(0, len1/spd_famima/3),
(tone_fa1, len1/spd_famima),#ファ
(tone_fa2, len1/spd_famima),#ファ
(tone_so2, len1/spd_famima),#ソ
(tone_fa2, len1/spd_famima),#ファ
(tone_ra1*tone_sharp, len1/spd_famima),#シb
(tone_re2*tone_sharp, len2/spd_famima),#ミb
(0, len1/spd_famima),
]

# 時代
spd_jidai = 1.0
jidai = [
(tone_do2*tone_sharp, len1/spd_jidai),#レb
(tone_re2*tone_sharp, len1/spd_jidai),#ミb
(tone_fa2, len3/spd_jidai),#ファー
(tone_fa2, len2/spd_jidai),#ファー
(tone_fa2, len1/spd_jidai),#ファ
(tone_fa2*tone_sharp, len3/spd_jidai),#ソbー
(tone_fa2, len1/spd_jidai),#ファ
(tone_re2*tone_sharp, len1/spd_jidai),#ミb
(tone_do2*tone_sharp, len1/spd_jidai),#レb
(tone_do2*tone_sharp, len3/spd_jidai),#レbー
(tone_do2, len1/spd_jidai),#ド
(tone_do2*tone_sharp, len1/spd_jidai),#レb
(tone_do2, len1/spd_jidai),#ド
(tone_ra1*tone_sharp, len3/spd_jidai),#シbー
(0, len1/spd_jidai),
(tone_ra1*tone_sharp, len1/spd_jidai),#シb
(tone_fa2*tone_sharp, len2/spd_jidai),#ソbー
(tone_fa2, len1/spd_jidai),#ファ
(tone_fa2*tone_sharp, len2/spd_jidai),#ソbー
(tone_fa2, len1/spd_jidai),#ファ
(tone_fa2*tone_sharp, len1/spd_jidai),#ソb
(tone_fa2, len1/spd_jidai),#ファ
(tone_re2*tone_sharp, len1/spd_jidai),#ミb
(tone_do2*tone_sharp, len1/spd_jidai),#レb
(tone_do2*tone_sharp, len1/spd_jidai),#レb
(tone_re2*tone_sharp, len1/spd_jidai),#ミb
(tone_fa2, len4/spd_jidai),#ファー
(tone_fa2*tone_sharp, len1/spd_jidai),#ソb
(tone_fa2, len1/spd_jidai),#ファ
(tone_re2*tone_sharp, len3/spd_jidai),#ミbー
(0, len1/spd_jidai),
(tone_fa2, len1/spd_jidai),#ファー
(tone_fa2*tone_sharp, len1/spd_jidai),#ソb
(tone_so2*tone_sharp, len3/spd_jidai),#ラbー
(tone_so2*tone_sharp, len2/spd_jidai),#ラbー
(tone_so2*tone_sharp, len1/spd_jidai),#ラb
(tone_ra2*tone_sharp, len3/spd_jidai),#シbー
(tone_fa2, len2/spd_jidai),#ファー
(tone_fa2, len1/spd_jidai),#ファ
(tone_so2*tone_sharp, len3/spd_jidai),#ラbー
(tone_so2*tone_sharp, len1/spd_jidai),#ラb
(tone_fa2*tone_sharp, len1/spd_jidai),#ソb
(tone_fa2, len1/spd_jidai),#ファ
(tone_so2*tone_sharp, len3/spd_jidai),#ラbー
(tone_fa2*tone_sharp, len3/spd_jidai),#ソbー
(0, len1/spd_jidai),
(tone_fa2, len1/spd_jidai),#ファ
(tone_fa2*tone_sharp, len1/spd_jidai),#ソb
(tone_so2*tone_sharp, len1/spd_jidai),#ラb
(tone_do2*tone_sharp, len1/spd_jidai),#レb
(tone_re2*tone_sharp, len1/spd_jidai),#ミb
(tone_fa2, len1/spd_jidai),#ファ
(tone_fa2*tone_sharp, len3/spd_jidai),#ソbー
(tone_fa2*tone_sharp, len1/spd_jidai),#ソb
(tone_fa2, len1/spd_jidai),#ファ
(tone_do2*tone_sharp, len1/spd_jidai),#ド
(tone_re2*tone_sharp, len3/spd_jidai),#ミbー
(tone_do2*tone_sharp, len4/spd_jidai),#レbー
]
jidai.extend(jidai)

# マリオ1UP
mario_oneup = [
(tone_mi2, len1/2),
(tone_do3, len1/2),
(tone_mi3, len1/2),
(tone_do3, len1/2),
(tone_re3, len1/2),
(tone_so3, len1/2)
]

def play_sound_with_beep_server(sounds, delay=len0, speed=1.0):
    sock_info = ('127.0.0.1', PORT_BEEP_SERVER)
    data = { 'sounds': sounds, 'delay':delay, 'speed':speed }
    json_data = json.dumps(data).encode('utf-8')
    sock_fo_beep_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_fo_beep_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock_fo_beep_server.sendto(json_data, sock_info)
