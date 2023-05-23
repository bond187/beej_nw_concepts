import sys
import socket
import os

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
            request = ""
            data = conn.recv(1024)
            done = False
            request = request + data.decode("ISO-8859-1")
            if "\r\n\r\n" in data.decode("ISO-8859-1"):
                done = True
            if not done:
                print("Data recieved:\n{}".format(data.decode("ISO-8859-1")))
            elif done:
                #print("Data recieved:\n{}".format(data.decode("ISO-8859-1")))
                print("Ok, all data has been received.")
                print("Here's what I have: ")
                print(request)
                print("Transmitting simple http response data...")
                #re_string = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"
                #conn.sendall(re_string.encode("ISO-8859-1"))

                re_lines = request.split("\r\n")
                get = re_lines[0]
                get_words = get.split(" ")
                path = get_words[1]
                re_file = os.path.split(path)[1]
                print("Retrieved file: {}".format(re_file))
                ext = os.path.splitext(re_file)[1]

                try:
                    with open("./{}".format(re_file)) as fp:
                        data = fp.read()   # Read entire file
                        if ext == ".txt":
                            MIME_type = "text/plain"
                            #print("File extension: {}".format(ext))
                            #print("MIME type: {}".format(MIME_type))
                        elif ext == ".html":
                            MIME_type = "text/html"
                            #print("File extension: {}".format(ext))
                            #print("MIME type: {}".format(MIME_type))
                        elif ext == ".jpeg" or ext == ".jpg":
                            MIME_type = "image/jpeg"
                except:
                    error_404 = "HTTP/1.1 404 Not Found\r\nContent-Type: {}\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found".format("text/plain")
                    conn.sendall(error_404.encode("ISO-8859-1"))
                    break
                    
                re_string = "HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(MIME_type, len(data), data)
                print(re_string)
                conn.sendall(re_string.encode("ISO-8859-1"))
                break
        conn.close()
        print("Waiting on new connection...")
    print("Connection closed!")
except KeyboardInterrupt:
    print("\nServing shutting down...")
    print("goodbye <3")
