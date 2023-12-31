
import time
from const_tables_1705047 import *


def print_spaced_hex_val(bv, bv_name=""):
    hex_str_list = []
    assert(bv.length()%8 == 0)
    if bv_name != "":
        print("Spaced Hex representation of vector : ", bv_name)
    for i in range(int(bv.length()/8)):
        print(bv[8*i:8*(i+1)].get_bitvector_in_hex(), end=" ")


def ret_ASCII_val(bv):
  assert(bv.length()%8 == 0)
  hex_str = ""
  for i in range(bv.length()//8):
    hex_str += bv[8*i:8*(i+1)].get_bitvector_in_ascii()
#   assert(len(hex_str) == 8)
  return hex_str


def sBoxStrVal(val, Inv = False):
    if Inv==True:
        sbox_val = InvSbox[val]
    else :
        sbox_val = Sbox[val]
    fstr = f'{sbox_val:x}'

    if len(fstr) < 2:
        fstr = "0"+fstr 
    assert(len(fstr)==2)
    return fstr


def subWord(bv_w, Inv = False):
    hex_str = ""
    assert(bv_w.length() == 32)
    for y in range(4):
        val = bv_w[8*y: 8*(y+1)].int_val()
        hex_str+=sBoxStrVal(val, Inv)
    assert(len(hex_str)==8)
    return BitVector(hexstring = hex_str)


def g(bv3, round):
    bv_new = bv3.deep_copy()
    bv_new << 8 # shift by one byte
    # print_spaced_hex_val(bv_new, "g() return_bv")
    return_bv = subWord(bv_new)
    # print_spaced_hex_val(return_bv, "g() return_bv")
    assert(round>0)
    return return_bv.__xor__(roundConst[round-1])


# the input is the cipher key that is used for encryption
def keyExpansion(cipherKey):
    start =  time.time()

    # converting all the text into bit vector
    bv_cipherKey = BitVector(textstring = cipherKey)

    # making sure that the key is a multiple of length 32
    assert (bv_cipherKey.length() % 32 == 0)

    # N is the total number of columns/ words
    N = bv_cipherKey.length() // 32


    col_size = 32 # 32 bits 
    keys = []

    init_key = []

    # convert the total text into chunks of 32 bits 
    # for AES 128, total columns would be 4
    # for AES 192, total columns would be 6 and so on 
    for i in range(N):
        init_key.append(bv_cipherKey[i*col_size: (i+1)*col_size])

    # determine the number of rounds corresponding to the cipher key length 
    num_rounds = 10 + int((bv_cipherKey.length()-128)/32)

    # use the formula in the link to calculate the words of expanded key 
    key_pool = []
    for i in range(4*(num_rounds+1)):
        if (i < N):
            key_pool.append(init_key[i])
        elif (i >= N and i%N == 0):
            key_pool.append(key_pool[i-N].__xor__(g(key_pool[i-1], i//N)))
        elif (i>=N and N > 6 and i%N == 4):
            key_pool.append(key_pool[i-N].__xor__(subWord(key_pool[i-1])))
        else :
            key_pool.append(key_pool[i-N].__xor__(key_pool[i-1]))
    
    end = time.time()
    key_mat = []

    assert(len(key_pool) == 4*(num_rounds + 1))

    for i in range(len(key_pool)):
        key_mat.append(key_pool[i])
        if i%4 == 3:
            keys.append(key_mat.copy())
            key_mat.clear()

    # N.B. : the number of columns are different for different versions of 
    # AES. But in all functions, only a group of 4 columns are used at a time
    # so in 192, even if you deal with 6 columns at first and build the next columns on top
    # of that, you would eventually break that up to take 4 columns at a time.
    
    return [keys, num_rounds, end-start] 
    

def getStateMatrix(plaintext):
    l = len(plaintext)*8
    upper_l = math.ceil(l/128)
    padding_length = 0
    if (l%128 != 0):
        padding_length = (upper_l*128 - l)//8
        plaintext += "_" * padding_length
    bv = BitVector(textstring = plaintext)
    state_matrices = []
    for i in range(upper_l):
        state_matrix = []
        for j in range(4):
            state_matrix.append(bv[i*128+j*32:i*128+(j+1)*32])
        state_matrices.append(state_matrix)
    return (state_matrices, padding_length)


def matrixSboxSubs(stateMatrix, Inv=False):
    new_mat = []
    for colMat in stateMatrix:
        assert(colMat.length()%32==0)
        new_mat.append(subWord(colMat, Inv))
    return new_mat


def cyclicRotateMatrix(stateMatrix):
    new_sm = []
    row_num = stateMatrix[0].length()//8
    for starting_col in range(len(stateMatrix)):
        hex_str = ""
        for j in range(row_num):
            bv = stateMatrix[(starting_col+j)%len(stateMatrix)]
            hex_str += bv[8*j:8*(j+1)].get_bitvector_in_hex()
        new_col_bv = BitVector(hexstring = hex_str)
        new_sm.append(new_col_bv)
    return new_sm


def cyclicInvRotateMatrix(stateMatrix):
    new_sm = []
    row_num = stateMatrix[0].length()//8
    for starting_col in reversed(range(len(stateMatrix))):
        hex_str = ""
        for j in range(row_num):
            bv = stateMatrix[(starting_col-j+len(stateMatrix))%len(stateMatrix)]
            hex_str += bv[8*j:8*(j+1)].get_bitvector_in_hex()
        new_col_bv = BitVector(hexstring = hex_str)
        new_sm.append(new_col_bv)
    new_sm = new_sm[::-1]
    return new_sm


def breakUpIntoHex(stateMatrix):
    num_cols = len(stateMatrix)
    num_rows = stateMatrix[0].length()//8
    assert(num_cols == 4 and num_rows == 4)
    new_stateMatrix = []
    for j in range(num_cols):
        new_col = []
        bv_col = stateMatrix[j]
        for i in range(num_rows):
            new_col.append(bv_col[8*i:8*(i+1)])
        new_stateMatrix.append(new_col)
    return new_stateMatrix 


def multiplyMatrix(stateMatrix, Mixer):
    num_cols = len(stateMatrix)
    num_rows = len(stateMatrix[0])
    assert(num_cols == 4 and num_rows == 4)
    mod = BitVector(bitstring='100011011')
    n = 8
    new_sm = []
    for j in range(num_cols):
        col_vec = stateMatrix[j]
        hex_str = ""
        for i in range(num_rows):
            mixer_vec = Mixer[i]
            all_new = []
            for elem in range(num_rows):
                bv_mixer = mixer_vec[elem]
                bv_sm = col_vec[elem]
                new_elem = bv_mixer.gf_multiply_modular(bv_sm, mod, n)
                all_new.append(new_elem)
            new_elem = BitVector(hexstring='00')
            for elem in all_new:
                new_elem = new_elem.__xor__(elem)
            hex_str += new_elem.get_bitvector_in_hex()
        new_col_bv = BitVector(hexstring = hex_str)
        new_sm.append(new_col_bv)
    return new_sm


def mixColumn(stateMatrix, inv=False):
    curr_mixer = Mixer
    if (inv == True):
        curr_mixer = InvMixer
    return multiplyMatrix(breakUpIntoHex(stateMatrix), curr_mixer)


def addRoundKey(stateMatrix, roundKey):
    assert(len(stateMatrix) == len(roundKey))
    new_sm = []
    for col_num in range(len(stateMatrix)):
        bv_sm = stateMatrix[col_num]
        bv_key = roundKey[col_num]
        new_sm.append(bv_sm.__xor__(bv_key))
    return new_sm


def readBits_and_GenSM(filename):
    char_bit_vects = []
    b = BitVector(filename = filename)
    while (b.more_to_read):
        bv_read = b.read_bits_from_file(8)
        char_bit_vects.append(bv_read)
    b.close_file_object()
    sz = len(char_bit_vects)*8
    padding_length = 0
    if (sz%128 != 0):
        upper_l = math.ceil(sz/128)
        padding_length = (upper_l*128 - sz)//8
        for x in range(padding_length):
            char_bit_vects.append(BitVector(textstring='_'))
    # merge into state matrix 
    state_matrices = []
    for i in range(len(char_bit_vects)//16):
        state_matrix = []
        for j in range(4):
            lmt = char_bit_vects[i*16+j*4:i*16+(j+1)*4]
            hex_str = ""
            for bv in lmt:
              hex_str += bv.get_bitvector_in_hex()
            state_matrix.append(BitVector(hexstring = hex_str))
        state_matrices.append(state_matrix)


    return (state_matrices, padding_length)


if __name__ == '__main__':
    # testing the utilities
    # pass 
    word = g(BitVector(hexstring='61746368'), 1)
    print_spaced_hex_val(word)
    print()
