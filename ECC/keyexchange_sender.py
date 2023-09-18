# -*- encoding: utf-8 -*-
'''
@File    :   keyexchange_sender.py
@Time    :   2023/05/06 19:39:03
@Author  :   zeroc 
'''
import sys
sys.dont_write_bytecode = True
import socket
from SM2 import *

# parameters of Elliptic Curve
p = 60275702009245096385686171515219896416297121499402250955537857683885541941187
a = 54492052985589574080443685629857027481671841726313362585597978545915325572248
b = 45183185393608134601425506985501881231876135519103376096391853873370470098074
E = EllipticCurve(a, b, p)
# the base point
G = E(29905514254078361236418469080477708234343499662916671209092838329800180225085,
      2940593737975541915790390447892157254280677083040126061230851964063234001314)
# the order of base point
n = 60275702009245096385686171515219896415919644698453424055561665251330296281527
# the ID of A and B
IDa = bytes.fromhex("414c494345313233405941484f4f2e434f4d")
IDb = bytes.fromhex("42494c4c343536405941484f4f2e434f4d")
# the private key of A
da = 50566520689538531512229984270522243112638550810818904689650258149112477052398
# the public key of B
PB = E(16432697982112952139694870046477384105563181197829916935694968456946518294339,
       37882130197454007051989042253319763547043709414936008810919953367622534695500)
# the random number of A
ra = 59540605051435204980914790089592329358787148029867248015672265760240703014243
RA = E(49170271750780605002340338109423982046800493186843347705654277232249705737200,
       6077618384723092770196272055827406523573877188367034612615140375118334770970)
sm2 = SM2(p, E, G, n)

HOST = "127.0.0.1"
PORT = 2333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print(f"[Sender]Listening on {HOST}:{PORT}")
conn, addr = s.accept()
print(f"[Sender]Connected by {addr}")
tmp = sm2.keyexchange_sender(da, PB, 1, ra, 256, IDa, IDb, 128)
RA = next(tmp)
RA = str(RA.x) + " " + str(RA.y)
conn.sendall(RA.encode()+b"\n")
print(f"[Sender]Send RA: {RA}")
date = conn.recv(1024)
RBx, RBy = map(int, date[:date.index(b"\n")].decode().split())
RB = E(RBx, RBy)
SB = date[date.index(b"\n")+1:]
print(f"[Sender]Received RB: {RB}")
print(b"[Sender]Received SB: " + SB)
tmp = sm2.keyexchange_sender(da, PB, 1, ra, 256, IDa, IDb, 128, RB, SB)
next(tmp)
SA = next(tmp)
conn.sendall(SA+b"\n")
print(b"[Sender]Send SA: " + SA)
status = conn.recv(1024)
print(f"[Sender]Received status: {status.decode()}")
conn.close()
s.close()
