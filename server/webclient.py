import socket
import sys

if len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
elif len(sys.argv) == 2:
    HOST = sys.argv[1]
    PORT = 80
else:
    print("Malformed input!!\nClient requires <HOST>, <PORT> arguments. You can also leave off the port number, in which case the client will default to port 80.")
    print("Goodbye.")
    exit()

CONNECT = (HOST, PORT)

s = socket.socket()
s.connect(CONNECT)

string_data = "GET / HTTP/1.1\r\nHost: {}:{}\r\nConnection: close\r\n\r\n".format(HOST, PORT)
iso_data = string_data.encode("ISO-8859-1")
s.sendall(iso_data)

while(True):
    r = s.recv(4096)
    if len(r) != 0:
        r_string = r.decode("ISO-8859-1")
        print(r_string)
    else:
        print("~Done~ Goodbye! <3")
        break
s.close()
