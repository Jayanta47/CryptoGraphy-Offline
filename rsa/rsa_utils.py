from BitVector import *
import time 

def gcd(a, b):
    while b!= 0:
        a, b = b, a%b
    return a 

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m


def gen_prime(bit_length):
    bv = BitVector(intVal = 0).gen_random_bits(bit_length)
    is_prime_prob = 0.0
    while(is_prime_prob < 0.98):
        is_prime_prob = bv.test_for_primality()
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
    d = modinv(e, lambda_n)
    if d == 1:
        raise Exception("modular inverse not found--> unusual case")
    
    assert( ((d%lambda_n)*(e%lambda_n))%lambda_n )
    end = time.time()
    return ((e, n), (d, n), end-start)