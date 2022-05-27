import socket
import os
from time import sleep

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "127.0.0.0"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "text.txt"
# get the file size
filesize = os.path.getsize(filename)

s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
print("filesize", filesize)
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
acck = s.recv(BUFFER_SIZE).decode()

text = "CanTheyArrangeTheFest?also is it feasible for an outsider to interfere a proper investigation needs to be carried out at buckingham palace the big one"

b = bytes(text, encoding='utf-8')
# with open(filename, "rb") as f:
#     while True:
#         # read the bytes from the file
#         bytes_read = f.read(BUFFER_SIZE)
#         if not bytes_read:
#             # file transmitting is done
#             break
#         # we use sendall to assure transimission in 
#         # busy networks
#         s.sendall(bytes_read)
        # update the progress bar
array_len = len(b)
curr_idx = 0
while(curr_idx < array_len):
    extract_len = BUFFER_SIZE
    if (curr_idx + BUFFER_SIZE) >= array_len:
        extract_len = array_len - curr_idx
    
    bytes_read = b[curr_idx: curr_idx + extract_len]
    curr_idx += extract_len
    s.sendall(bytes_read)

# close the socket
s.close()