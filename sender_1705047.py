import socket
import json
from encrypt_1705047 import encrypt
from rsa_utils_1705047 import key_generation, readBits
from rsa_encrypt_1705047 import rsa_encrypt
from rsa_utils_1705047 import ret_ASCII_val
import time 


BUFFER_SIZE = 4096 # send 4096 bytes each time step


host, port = "127.0.0.0" , 5001

s = socket.socket()

def send_json_message(json_message):
    s.sendall("JSON_INCOMING".encode("utf-8"))
    message = (json.dumps(json_message)).encode()
    send_ack = s.recv(BUFFER_SIZE).decode()
    # print(send_ack)
    assert(send_ack == "SEND_JSON")
    s.sendall(message)
    json_ack = s.recv(BUFFER_SIZE).decode()
    assert(json_ack == "META_RECEIVED")



def sendASCIIstream(data):
    s.sendall("DATA_INCOMING".encode("utf-8"))
    data_send_ack = s.recv(BUFFER_SIZE).decode()
    assert(data_send_ack == "SEND_DATA")
    b = bytes(data, encoding = 'utf-8')
    array_len = len(b)
    curr_idx = 0
    while(curr_idx < array_len):
        extract_len = BUFFER_SIZE
        if (curr_idx + BUFFER_SIZE) >= array_len:
            extract_len = array_len - curr_idx
        
        bytes_read = b[curr_idx: curr_idx + extract_len]
        curr_idx += extract_len
        s.sendall(bytes_read)
    ack = s.recv(BUFFER_SIZE).decode()
    assert(ack == "ACK")





if __name__ == "__main__":
    print("Welcome Alice")
    

    # k = int(input("Enter size of RSA key, K: "))
    # aes_key_length = int(input("AES Key Length: "))
    # aes_cipher_key = str(input("AES Cipher Key: ")).strip('\n')
    # ans = int(input("Enter type of Input: 1. Plaintext 2. File :"))
    # text = ""
    # filename = ""
    # if ans == 1:
    #     text = str(input("Enter Plaintext: ")).strip("\n")
    #     input_type = "plaintext"
    # else: 
    #     filename = str(input("Enter Filename: ")).strip("\n")
    #     input_type = "file"

    k = 16
    aes_key_length = 16
    aes_cipher_key = "BUET CSE17 BATCH"
    text = "CanTheyDoTheirFe"
    input_type = "file"
    filename = "pic2.png"

    

    

    

    # resizing the aes keuy if it does not match the required size

    if len(aes_cipher_key) > aes_key_length:
        aes_cipher_key = aes_cipher_key[0:aes_key_length]
    elif len(aes_cipher_key) < aes_key_length:
        x = aes_key_length - len(aes_cipher_key)
        aes_cipher_key = aes_cipher_key + " "*x

    # RSA key generation 
    (public_key, private_key, time_) = key_generation(k)

    # encrypt the aes key 
    (ciphertext, enc_time) = rsa_encrypt(public_key, readBits(aes_cipher_key))

    # write the aes key into polling folder
    private_key_file = open("DO_NOT_OPEN/PK.txt", "w")
    (d, n) = private_key
    private_key_file.write(str(d)+ " " + str(n))
    private_key_file.close()

    # convert the encrypted key into ASCII 
    aes_enck_key_str = ""
    aes_key_delimeter = "/"
    for c in ciphertext:
        aes_enck_key_str += str(c)
        aes_enck_key_str += aes_key_delimeter

    (encrypted_blocks, padding_length, ke_ex_time, enc_ex_time) = encrypt(aes_cipher_key, {
        'type' : input_type,
        'filename' : filename,
        'plaintext' : text
    })

    # convert the encrypted blocks into encrypted text (ASCII form) 
    temp_val = ""
    encrypted_text = ""
    for block in encrypted_blocks:
        for col in block:
            temp_val += ret_ASCII_val(col)
        encrypted_text += temp_val
        temp_val = ""

    # generate the metadata to send the receiver 
    MetaData = {
        'type' : input_type,
        'filename' : filename, 
        'length': len(encrypted_text),
        'padding_length': padding_length, 
        'aes_key': aes_enck_key_str,
        'aes_key_delimiter': aes_key_delimeter,
        'rsa_public_key' : str(public_key),

    }

    
    

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    start = time.time()
    send_json_message (MetaData)
    sendASCIIstream (encrypted_text)
    end = time.time()

    file_write_ack = s.recv(BUFFER_SIZE).decode()
    assert(file_write_ack == "DONE")
    s.sendall("END".encode("utf-8"))

    if input_type == "text":
        rec_file = open("DO_NOT_OPEN/decrypted_text.txt")
        file_text = ""
        for line in rec_file:
            file_text += line
        if (file_text == text):
            print("Deciphered File Matches Successfully")

    print("Execution Time: ")
    print("Key Scheduling (seconds) :", ke_ex_time)
    print("Encryption Time (seconds) :", enc_ex_time)
    print("Data Transmission Time (seconds) :", end- start)

    s.close()








# b = bytes(text, encoding='utf-8')
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
# array_len = len(b)
# curr_idx = 0
# while(curr_idx < array_len):
#     extract_len = BUFFER_SIZE
#     if (curr_idx + BUFFER_SIZE) >= array_len:
#         extract_len = array_len - curr_idx
    
#     bytes_read = b[curr_idx: curr_idx + extract_len]
#     curr_idx += extract_len
#     s.sendall(bytes_read)

# close the socket