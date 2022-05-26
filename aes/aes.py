from aes_utils import print_spaced_hex_val, ret_ASCII_val
from encrypt import encrypt
from decrypt import decrypt

# cipherKey = "BUET CSE17 Batch"
# cipherKey = "Thats my Kung Fu"
cipherKey = "Thats my Kung Fu Panda you get o"
# cipherKey = "Thats my Kung Fu Panda o"

encrypted_blocks = encrypt(cipherKey, 'Two One Nine Two')

ascii_val = ""
for block in encrypted_blocks:
    for col in block:
        print_spaced_hex_val(col)
    print("\nASCII value: ", end="")
    for col in block:
        ascii_val += ret_ASCII_val(col)
    print(ascii_val)


decrypted_blocks = decrypt(cipherKey, ascii_val)

dec_ascii_val = ""
for block in decrypted_blocks:
    for col in block:
        print_spaced_hex_val(col)
    print("\nASCII value: ", end="")
    for col in block:
        dec_ascii_val += ret_ASCII_val(col)
    print(dec_ascii_val)