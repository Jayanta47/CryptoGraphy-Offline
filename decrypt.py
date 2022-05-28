from aes_utils import *
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