import sys
import random
from time import time
from itertools import repeat


def slice(input, size):
    return [input[i:i+size] for i in range(0, len(input), size)]

def bin_v(val, bitsize):
    bin_val = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(bin_val) > bitsize:
        raise ValueError("Value exceeded the expected size")
    while len(bin_val) < bitsize:
        bin_val = "0" + bin_val
    return bin_val

def str_bin(p_text): # List of bits forming a string
    string = []
    for byte in p_text:
        bin_val = bin_v(byte, 8)
        string.extend([int(bit) for bit in list(bin_val)])
    return string

def str_num(p_text): # Numerical value of string
    l = "".join([str(b) for b in str_bin(p_text)])
    return int(l, 2)

def num_str(num, t_len): # String representation of a number
    return "".join([chr((num >> s) & 0xFF) for s in reversed(range(0, t_len << 3, 8))])

def bin_str(string): # String reformed from list of bits
    return ''.join([chr(int(i,2)) for i in [''.join([str(j) for j in bytes]) for bytes in  slice(string,8)]])

def gcd(m, b):
    while b != 0:
        m, b = b, m % b
    return m

def ext_gcd(m, b):
    a1, a2 = 1, 0
    b1, b2 = 0, 1
    while b != 0:
        q, m, b = m // b, b, m % b
        a1, a2 = a2, a1 - q * a2
        b1, b2 = b2, b1 - q * b2
    return  m, a1, b1

def mod_inv(m, b):
    m, a, _ = ext_gcd(m, b)
    if m == 1:
        return a % b

def rab_mil(num, acc=8):
    try:
        int(num)
    except ValueError:
        raise ValueError("Invalid format. Input must be a positive integer")
    if int(num) != num or num < 0:
        raise ValueError("Non integer number. Input must be a positive integer")
    if num < 10:
        return [False, False, True, True, False, True, False, True, False, False][num]
    elif num & 1 == 0:
        return False
    else:
        j, d = 0, num - 1
        while d & 1 == 0:
            j+=1
            d >>= 1
        for _ in repeat(None, acc):
            n = random.randrange(2, num)
            p = pow(n, d, num)
            if p != 1 and p + 1 != num:
            # if p == 1 or p  == num - 1:
                for i in range(1, j):
                    p = pow(p, 2, num)
                    if p == 1:
                        return False
                    elif p == num - 1:
                        n = 0
                        break
                if n:
                    return False
        return True


def prm_gen(bits):
    p = random.getrandbits(bits)
    while not rab_mil(p):
        p = random.getrandbits(bits)
    return p

def prm_gen_old(key_len): # 63
    prime = False
    while not prime:
        p = random.randint(2 ** (key_len - 1), 2 ** key_len)
        if rab_mil(p):
            return p

# public, private = generate_keypair(p, q)

def gen_key(p, q):
    phi, mod = (p - 1) * (q - 1), p * q
    enc = random.randrange(1, phi)
    g = gcd(enc, phi)
    while g != 1:
        enc = random.randrange(1, phi)
        g = gcd(enc, phi)
    return (enc, mod_inv(enc, phi), mod)

def init(bits):
    p = prm_gen(bits)
    q = prm_gen(bits)
    return gen_key(p, q)


def encrypt(prv_key, mod, p_text):
    return [pow(ord(char), prv_key, mod) for char in p_text]

def decrypt(pub_key, mod, c_text):
    return ''.join([chr(pow(char, pub_key, mod)) for char in c_text])

# encrypt(private, message)
# decrypt(public, encrypted_msg)
    #if mod < 65537:
    #    return (3, mod_inv(3, phi), mod)
    #else:
    #    return (65537, mod_inv(65537, phi), mod)
