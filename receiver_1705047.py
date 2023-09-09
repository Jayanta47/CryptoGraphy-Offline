import json
import socket
from rsa_decrypt_1705047 import rsa_decrypt
from decrypt_1705047 import decrypt
from aes_utils_1705047 import ret_ASCII_val
from BitVector import *



# device's IP address
SERVER_HOST = "127.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 4096


s = socket.socket()

client_socket = socket.socket()


def decrypt_data(encrypted_text, MetaData):
    aes_str_key = MetaData["aes_key"]
    delimiter = MetaData["aes_key_delimiter"]
    aes_str_key_list = aes_str_key.split(delimiter)
    aes_str_key_list = aes_str_key_list[:-1]
    # print(aes_str_key_list)
    aes_str_key_list = [int(i) for i in aes_str_key_list]
    private_key_file = open("DO_NOT_OPEN/PK.txt", "r")
    (d, n) = private_key_file.readline().strip().split()
    d, n = int(d), int(n)

    (decrypt_text_bv, rsa_dec_time) = rsa_decrypt((d, n), aes_str_key_list)

    aes_key = decrypt_text_bv.get_bitvector_in_ascii()
    # print(aes_key)
    (decrypted_blocks, dec_ex_time) = decrypt(aes_key, encrypted_text)
    dec_ascii_val = ""
    for block in decrypted_blocks:
        for col in block:
            dec_ascii_val += ret_ASCII_val(col)
    padding_length = MetaData['padding_length']
    if padding_length != 0:
        dec_ascii_val =  dec_ascii_val[:-padding_length]
    bv_write = BitVector(textstring = dec_ascii_val)
    if MetaData['type'] == "text":
        filename = "text.txt"
    else:
        filename = MetaData["filename"]

    dec_file_out = open("DO_NOT_OPEN/decrypted_"+ filename, "wb")
    bv_write.write_to_file(dec_file_out)
    dec_file_out.close()
    print("Written to file :", filename)
    print("Execution Time:")
    print("AES cipher Key Decryption Time: ", rsa_dec_time)
    print("Data Decryption Time: ", dec_ex_time)
    client_socket.sendall("DONE".encode("utf-8"))


def receive_JSON_meta():
    client_socket.sendall("SEND_JSON".encode("utf-8"))
    MetaData = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    MetaData = json.loads(MetaData)
    # print(MetaData)
    client_socket.sendall("META_RECEIVED".encode("utf-8"))
    return MetaData


def receive_enc_data(MetaData):
    client_socket.sendall("SEND_DATA".encode("utf-8"))
    encrypted_text = ""
    data_length = MetaData['length']
    while data_length > len(encrypted_text):
        bytes_read = client_socket.recv(BUFFER_SIZE)

        encrypted_text += bytes_read.decode(errors="replace")
        # print(len(encrypted_text))
    client_socket.sendall("ACK".encode("utf-8"))
    # print("done rec")
    decrypt_data(encrypted_text, MetaData)

if __name__ == "__main__":
    print("Welcome Bob")
    s.bind((SERVER_HOST, SERVER_PORT))

    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    client_socket, address = s.accept() 

    print(f"[+] {address} is connected.")
    MetaData = {}
    while True:
        msg = client_socket.recv(BUFFER_SIZE).decode()
        if msg == "JSON_INCOMING":
            MetaData = receive_JSON_meta()
        elif msg == "DATA_INCOMING" :
            receive_enc_data(MetaData)
        elif msg == "END":
            break
    
    client_socket.close()
    s.close()




# received = client_socket.recv(BUFFER_SIZE).decode()
# # remove absolute path if there is
# filename = os.path.basename(filename)
# # convert to integer
# filesize = int(filesize)

# client_socket.send("ACK".encode())
# with open("rr"+filename, "wb") as f:
#     while True:
#         # read 1024 bytes from the socket (receive)
#         bytes_read = client_socket.recv(BUFFER_SIZE)
#         if not bytes_read:    
#             # nothing is received
#             # file transmitting is done
#             break
#         # write to the file the bytes we just received
#         f.write(bytes_read)


# # close the client socket
# client_socket.close()
# # close the server socket
# s.close()

