from aes_utils import print_spaced_hex_val, ret_ASCII_val
from encrypt import encrypt
from decrypt import decrypt
from BitVector import *

parameters = {
    'key_length' : 32,
    'cipherKey' : "BUET CSE17 Batch Festival is one",
    'input_data' : {
        'type' : "file",
        'filename' : 'text.txt',
        'plaintext' : "CanTheyDoTheirFest?"
    }
}

ans = input("Use Default settings? [y/n]")
if ans == "n" or ans == "N" or ans == "No":
    parameters['key_length'] = int(input("Key Length: "))
    parameters['cipherKey'] = str(input("Cipher Key: ")).strip('\n')
    if len(parameters['cipherKey']) > parameters["key_length"]:
        l = parameters["key_length"]
        key = parameters['cipherKey']
        key = key[0:l]
        parameters['cipherKey'] = key
    elif len(parameters['cipherKey']) < parameters["key_length"]:
        l = parameters["key_length"]
        key = parameters['cipherKey']
        x = l - len(key)
        key = key + " "*x
        parameters['cipherKey'] = key
    parameters['input_data']['type'] = "text" if int(input("Type of Input: 1.Plaintext 2.File ")) == 1 else "file"
    if parameters['input_data']['type'] == "text":
        parameters['input_data']['plaintext'] = str(input("Enter PlainText: ")).strip()
    else :
        parameters['input_data']['filename'] = str(input("Enter FileName: "))

print("Proceeding...")
print(parameters)

print("\n\n")

if parameters['input_data']['type'] == "text":
    print("Plain Text:")
    print(parameters['input_data']['plaintext'], "[In ASCII]")
    print_spaced_hex_val (
        BitVector(textstring = parameters['input_data']['plaintext']) )
    print(
        "[In Hex]"
    )

print()

print("Key:")
print(parameters['cipherKey'], "[In ASCII]")
print_spaced_hex_val (
    BitVector(textstring = parameters['cipherKey']) )
print(
    "[In Hex]"
)


(encrypted_blocks, padding_length, ke_ex_time, enc_ex_time) = encrypt(parameters["cipherKey"], parameters["input_data"])

if parameters['input_data']['type'] == "text":
    
    print("\n\nCipher Text")
    ascii_val = ""
    encrypted_text = ""
    for block in encrypted_blocks:
        for col in block:
            print_spaced_hex_val(col)
        
        for col in block:
            ascii_val += ret_ASCII_val(col)
        encrypted_text += ascii_val
        ascii_val = ""
    print(" [In HEX] [With Padding]")
    print("ASCII value: ")
    print(encrypted_text)

    (decrypted_blocks, dec_ex_time) = decrypt(parameters["cipherKey"], encrypted_text)

    print("\n\nDeciphered Text:")
    dec_ascii_val = ""
    for block in decrypted_blocks:
        for col in block:
            print_spaced_hex_val(col)
        # print("\nASCII value: ", end="")
        for col in block:
            dec_ascii_val += ret_ASCII_val(col)

    print(" [In HEX]{With Padding]")
    print("ASCII value: ")
    if padding_length == 0:
        print(dec_ascii_val)
    else:
        print(dec_ascii_val[:-padding_length])

elif parameters['input_data']['type'] == "file":
    ascii_val = ""
    encrypted_text = ""
    for block in encrypted_blocks:
        for col in block:
            ascii_val += ret_ASCII_val(col)
        encrypted_text += ascii_val
        ascii_val = ""
    filename = parameters['input_data']['filename']
    # print(encrypted_text)
    enc_file_out = open("aes_enc_"+filename, "w")
    enc_file_out.write(encrypted_text)
    enc_file_out.close()
    (decrypted_blocks, dec_ex_time) = decrypt(parameters["cipherKey"], encrypted_text)
    dec_ascii_val = ""
    for block in decrypted_blocks:
        for col in block:
            dec_ascii_val += ret_ASCII_val(col)
    if padding_length != 0:
        dec_ascii_val =  dec_ascii_val[:-padding_length]
    bv_write = BitVector(textstring = dec_ascii_val)

    dec_file_out = open("aes_dec_"+ filename, "wb")
    bv_write.write_to_file(dec_file_out)
    dec_file_out.close()
    
print("\n\n")
print("Execution time:")
print("Key Scheduling (seconds) :", ke_ex_time)
print("Encryption Time (seconds) :", enc_ex_time)
print("Decryption time (seconds) :", dec_ex_time)



# cipherKey = "BUET CSE17 Batch"
# cipherKey = "Thats my Kung Fu"
# cipherKey = "Thats my Kung Fu Panda you get o"
# cipherKey = "Thats my Kung Fu Panda o"

# (encrypted_blocks, padding_length) = encrypt(cipherKey, 'Two One Nine Two for the win hola')


# (encrypted_blocks, padding_length) = encrypt(cipherKey, {'type':'text', 
#                                             'plaintext': 'Two One Nine Two for the win hola'})