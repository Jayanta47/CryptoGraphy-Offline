from aes_utils_1705047 import *
import time

def decrypt(cipherKey, cipherText):
  [keys, num_rounds, ex_time] = keyExpansion(cipherKey)
  (state_matrices, padding_length) = getStateMatrix(cipherText)
  decrypted_blocks = []

  start = time.time()
  for sm in state_matrices:
    stateMatrix = sm
    for round in range(num_rounds+1):
      if round == 0:
        stateMatrix = addRoundKey(stateMatrix, keys[num_rounds-round])
        stateMatrix = cyclicInvRotateMatrix(stateMatrix)
        stateMatrix = matrixSboxSubs(stateMatrix, True)
      elif round == num_rounds:
        stateMatrix = addRoundKey(stateMatrix, keys[num_rounds-round])
      else:
        stateMatrix = addRoundKey(stateMatrix, keys[num_rounds-round])
        stateMatrix = mixColumn(stateMatrix, True)
        stateMatrix = cyclicInvRotateMatrix(stateMatrix)
        stateMatrix = matrixSboxSubs(stateMatrix, True)
    decrypted_blocks.append(stateMatrix)
  end = time.time()
  return (decrypted_blocks, end-start)

if __name__ == "__main__":
  cipherKey = "BUET CSE17 Batch"
  bv = BitVector(hexstring="27ddffcfcd41984de8423b847004badb")
  cipherText = bv.get_bitvector_in_ascii()
  print("Cipher Text: ", cipherText)

  (decrypted_blocks, ex_time) = decrypt(cipherKey, cipherText)

  decrypted_text = ""
  temp_val = ""
  for block in decrypted_blocks:
      for col in block:
          temp_val += ret_ASCII_val(col)
      decrypted_text += temp_val
      temp_val = ""

  print("Decrypted Text: ", decrypted_text)