# -*- encoding: utf-8 -*-
'''
@File    :   keyexchange_receiver.py
@Time    :   2023/05/06 19:39:29
@Author  :   zeroc 
'''
import sys
sys.dont_write_bytecode = True
from SM2 import *
import socket

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
# the private key of B
db = 42612540250945654498121385670255525590153896720640460925220400643337899096915
# the public key of A
PA = E(21981408064932226135301202771561762143335985281913055880427170456330466891349,
       28028589283980403447494504310906074608090471180368249734410319713138692249995)
# the random number of B
rb = 23516966180244969484344201605495627677787965516464210688348072152616195792000
sm2 = SM2(p, E, G, n)

HOST = "127.0.0.1"
PORT = 2333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(f"[Recevier]Connect to {HOST}:{PORT}")
RAx, RAy = map(int, s.recv(1024).strip().decode().split())
RA = E(RAx, RAy)
print(f"[Recevier]Receive RA: {RA}")
tmp = sm2.keyexchange_receiver(db, PA, RA, 1, rb, 256, IDa, IDb, 128)
RB, SB = next(tmp)
RB = str(RB.x) + " " + str(RB.y)
s.sendall(RB.encode() + b"\n" + SB)
print(f"[Recevier]Send RB: {RB}")
print(b"[Recevier]Send SB: " + SB)
SA = s.recv(1024).strip()
print(b"[Recevier]Receive SA: " + SA)
tmp = sm2.keyexchange_receiver(db, PA, RA, 1, rb, 256, IDa, IDb, 128, SA)
next(tmp)
status = next(tmp)
if status:
      print("[Recevier]Key exchange successfully!")
      s.sendall(b"Key exchange successfully!")
      s.close()
else:
      print("[Recevier]Key exchange failed!")
      s.sendall(b"Key exchange failed!")
      s.close()