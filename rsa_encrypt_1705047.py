import time 

def rsa_encrypt(key, data_bv_list):
    start = time.time()
    (e, n) = key 
    cipher_list = []
    for bv in data_bv_list:
        m = bv.int_val()
        cipher_list.append(pow(m, e, n))
    end = time.time()
    return (cipher_list, end - start)