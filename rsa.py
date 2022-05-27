from rsa_encrypt import rsa_encrypt
from rsa_decrypt import rsa_decrypt
from rsa_utils import key_generation, readBits, ret_ASCII_val


rsa_meta = {
    'public': (45097, 2571216841),
    'private': (2123962321, 2571216841)
}

(rsa_meta['public'], rsa_meta['private'], time_) = key_generation(128)

print("key generation time:", time_)

print("public key", rsa_meta['public'], "\n", "private key", rsa_meta['private'])

text = "CanTheyArrangeTheFest?"

ciphertext = rsa_encrypt(rsa_meta['public'], readBits("text.txt", True))

for c in ciphertext:
    print(c)

decrypt_text_bv = rsa_decrypt(rsa_meta['private'], ciphertext)

# str_ascii = ""
# for d in decrypt_text_bv:
#     str_ascii += ret_ASCII_val(d)

print(decrypt_text_bv.get_bitvector_in_ascii())