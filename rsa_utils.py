from BitVector import *
import time 

def ret_ASCII_val(bv):
    assert(bv.length()%8 == 0)
    hex_str = ""
    for i in range(bv.length()//8):
        hex_str += bv[8*i:8*(i+1)].get_bitvector_in_ascii()
    #   assert(len(hex_str) == 8)
    return hex_str


def gcd(a, b):
    while b!= 0:
        a, b = b, a%b
    return a 

# def egcd(a, b):
#     if a == 0:
#         return (b, 0, 1)
#     else:
#         g, y, x = egcd(b % a, a)
#         return (g, x - (b // a) * y, y)

# def modinv(a, m):
#     g, x, y = egcd(a, m)
#     if g != 1:
#         return -1
#     else:
#         return x % m


def gen_prime(bit_length):
    is_prime_prob = 0.0
    while(is_prime_prob < 0.98):
        bv = BitVector(intVal = 0).gen_random_bits(bit_length)
        is_prime_prob = bv.test_for_primality()
        # print(is_prime_prob)
    return bv.int_val()


def key_generation(k):
    start = time.time()
    p = gen_prime(k//2)
    
    q = p
    while(q == p):
        q = gen_prime(k//2)

    if p < q:
        p, q = q, p
    
    n = p*q
    lambda_n = ((p-1)*(q-1)) // gcd(p-1, q-1)

    e = 2**16+1
    if (e > lambda_n):
        e = 2**8 + 1
    assert(gcd(e, lambda_n) == 1)

    # d = modinv(e, lambda_n)
    d = BitVector(intVal = e).multiplicative_inverse(BitVector(intVal = lambda_n)).int_val()
    if d is None:
        raise Exception("modular inverse not found--> unusual case")
    
    assert( ((d%lambda_n)*(e%lambda_n))%lambda_n )
    end = time.time()
    return ((e, n), (d, n), end-start)


def readBits(message, input_from_file = False):
    all_bit_vects = []
    if input_from_file == True:
        b = BitVector(filename = message)
        while (b.more_to_read):
            bv_read = b.read_bits_from_file(8)
            all_bit_vects.append(bv_read)
        b.close_file_object()
    else :
        for c in message:
            b = BitVector(textstring = c)
            all_bit_vects.append(b)
    
    return all_bit_vects
