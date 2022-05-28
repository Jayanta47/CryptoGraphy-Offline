from rsa_encrypt import rsa_encrypt
from rsa_decrypt import rsa_decrypt
from rsa_utils import key_generation, readBits


rsa_meta = {
    'public': (45097, 2571216841),
    'private': (2123962321, 2571216841)
}

k = int(input("Enter size of K: "))

ans = int(input("Enter type of Input: 1. Plaintext 2. File: "))

if ans == 1:
    text = str(input("Enter Plaintext: ")).strip("\n")
else: 
    filename = str(input("Enter Filename: "))


(rsa_meta['public'], rsa_meta['private'], time_) = key_generation(k)

if ans == 1:
    (ciphertext, enc_time) = rsa_encrypt(rsa_meta['public'], readBits(text))
    (decrypt_text_bv, dec_time) = rsa_decrypt(rsa_meta['private'], ciphertext)
    print("Plaintext: ")
    print(text, "[In ASCII]")
    
    print("public key: ", rsa_meta['public']) 
    print("private key: ", rsa_meta['private'])

    print("\nCipherText: ")
    for c in ciphertext:
        print(c, end = ", ")

    print("\nDeciphered Text:")

    print(decrypt_text_bv.get_bitvector_in_ascii())
    
else:
    (ciphertext, enc_time) = rsa_encrypt(rsa_meta['public'], readBits(filename, True))
    enc_output_file = open("enc_" + filename, "w")
    for c in ciphertext:
        enc_output_file.write(str(c))
        enc_output_file.write(" ")
    enc_output_file.close()
    (decrypt_text_bv, dec_time) = rsa_decrypt(rsa_meta['private'], ciphertext)
    dec_out_file = open("dec_" + filename, "wb")
    # dec_out_file.write(decrypt_text_bv.get_bitvector_in_ascii())
    decrypt_text_bv.write_to_file(dec_out_file)
    dec_out_file.close()

print("Execution Time:")
print("Key generation time:", time_)
print("Encryption Time: ", enc_time)
print("Decryption Time: ", dec_time)




