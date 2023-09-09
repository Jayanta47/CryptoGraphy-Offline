from BitVector import *
import time

def rsa_decrypt(key, cipher_text):
    start = time.time()
    (d, n) = key

    hex_str = ""
    for c in cipher_text:
        m = pow(c, d, n)
        # print(m)
        hex_str += BitVector(intVal = m,size=8).get_bitvector_in_ascii()
    
    end = time.time()
    return (BitVector(textstring = hex_str), end - start)