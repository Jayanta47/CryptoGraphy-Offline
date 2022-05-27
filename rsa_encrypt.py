def rsa_encrypt(key, data_bv_list):
    (e, n) = key 
    cipher_list = []
    for bv in data_bv_list:
        m = bv.int_val()
        cipher_list.append(pow(m, e, n))
    return cipher_list