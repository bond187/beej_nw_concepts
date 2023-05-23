import datetime
import socket

def nist_time():
    HOST = "time.nist.gov"
    PORT = 37

    #Loop in case NIST returns 0 for time, in which case we try again.
    while True:
        #Create socket, connect to NIST time server, receive data, close connection
        s = socket.socket()
        s.connect((HOST, PORT))
        r = s.recv(4096)
        s.close()

        #Convert received data from big-endian bytes into an integer and return it 
        r_int = int.from_bytes(r, "big")
        if r_int != 0:
            break
    return r_int

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(datetime.datetime.now().strftime("%s"))
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

print("NIST Time: {}\nSystem Time: {}".format(nist_time(), system_seconds_since_1900()))
