import sys
import socket
from time import sleep

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 28333

bind_tuple = ('', PORT)

print("Server initializing...")
print("Listening on port: {}".format(PORT))

try:
    s = socket.socket()
    s.bind(bind_tuple)

    while(True):
        s.listen()
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        while(True):
            data = conn.recv(1024)
            done = False
            if "\r\n\r\n" in data.decode("ISO-8859-1"):
                done = True
            if not done:
                print("Data recieved:\n{}".format(data.decode("ISO-8859-1")))
            elif done:
                print("Data recieved:\n{}".format(data.decode("ISO-8859-1")))
                print("Ok, all data has been received.")
                print("Transmitting simple http response data...")
                re_string = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"
                conn.sendall(re_string.encode("ISO-8859-1"))
                break
        conn.close()
        print("Waiting on new connection...")
    print("Connection closed!")
except KeyboardInterrupt:
    print("\nServing shutting down...")
    print("goodbye <3")
