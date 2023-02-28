import socket
from time import time, gmtime, ctime
from os import rename

sock = socket.socket()
ip = "192.168.43.105"
port = 9999
sock.bind((ip, port))

sock.listen(10)

while True:
    conn, addr = sock.accept()
    print("connected:", addr)
    name_f = (conn.recv(1024)).decode('utf-8')
    file = open('sent/' + name_f, 'wb')
    while True:
        l = conn.recv(1024)
        file.write(l)
        if not l:
            print("file received")
            break
    file.close()
    t = time()
    gm = gmtime(t)
    c = ctime(t).split(" ")[3]
    name = name_f.split(".")
    name = name[0] + f"{gm.tm_mday}-{gm.tm_mon}-{gm.tm_year}-{c}." + name[1]
    name = name.replace(":", "-", 2)
    rename("C:\\Users\\artem\\PycharmProjects\\pythonProject\\sent\\motion.avi",
           "C:\\Users\\artem\\PycharmProjects\\pythonProject\\sent\\" + name)
    if 0xff == ord('q'):
        break

sock.close()
