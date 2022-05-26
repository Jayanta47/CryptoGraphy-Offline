from aes_utils import *

def encrypt(cipherKey, plainText):
  [keys, num_rounds] = keyExpansion(cipherKey)
  state_matrices = getStateMatrix(plainText)
  encrypted_blocks = []

  for sm in state_matrices:
    stateMatrix = sm
    for round in range(num_rounds+1):
      if round == 0:
        stateMatrix = addRoundKey(stateMatrix, keys[round])
      elif round == num_rounds:
        stateMatrix = matrixSboxSubs(stateMatrix)
        stateMatrix = cyclicRotateMatrix(stateMatrix)
        stateMatrix = addRoundKey(stateMatrix, keys[round])
      else:
        stateMatrix = matrixSboxSubs(stateMatrix)
        stateMatrix = cyclicRotateMatrix(stateMatrix)
        stateMatrix = mixColumn(stateMatrix)
        stateMatrix = addRoundKey(stateMatrix, keys[round])
    encrypted_blocks.append(stateMatrix)
  return encrypted_blocks

if __name__ == "__main__":
  encrypted_blocks = encrypt("BUET CSE17 Batch", 'CanTheyDoTheirFe')

  ascii_val = ""
  for block in encrypted_blocks:
    for col in block:
      print_spaced_hex_val(col)
    print("\nASCII value: ", end="")
    for col in block:
      ascii_val += ret_ASCII_val(col)
    print(ascii_val)