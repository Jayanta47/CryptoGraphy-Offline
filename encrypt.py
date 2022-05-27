from aes_utils import *

def encrypt(cipherKey, data):
  [keys, num_rounds] = keyExpansion(cipherKey)
  if data['type'] == "file":
        filename = data['filename']
        (state_matrices, padding_length) = readBits_and_GenSM(filename)
  else :
    plainText = data['plaintext']
    (state_matrices, padding_length) = getStateMatrix(plainText)
  encrypted_blocks = []

  print(len(state_matrices))
  i = 0
  for sm in state_matrices:
    print(i)
    i = i + 1
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
  return (encrypted_blocks, padding_length)

if __name__ == "__main__":
  (encrypted_blocks, padding_length) = encrypt("BUET CSE17 Batch", 'CanTheyDoTheirFe')

  ascii_val = ""
  for block in encrypted_blocks:
    for col in block:
      print_spaced_hex_val(col)
    print("\nASCII value: ", end="")
    for col in block:
      ascii_val += ret_ASCII_val(col)
    print(ascii_val)