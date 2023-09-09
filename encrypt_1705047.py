from aes_utils_1705047 import *
import time 

def encrypt(cipherKey, data):
  [keys, num_rounds, ex_time] = keyExpansion(cipherKey)
  # for key in keys:
  #   for col in key:
  #     print_spaced_hex_val(col)

  #   print("")

  if data['type'] == "file":
        filename = data['filename']
        (state_matrices, padding_length) = readBits_and_GenSM(filename)
  else :
    plainText = data['plaintext']
    (state_matrices, padding_length) = getStateMatrix(plainText)
  encrypted_blocks = []

  # print(len(state_matrices))
  # i = 0
  start = time.time()
  for sm in state_matrices:
    # print(i)
    # i = i + 1
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
  end = time.time()
  return (encrypted_blocks, padding_length, ex_time, end-start)

if __name__ == "__main__":
  data = {
        'type' : "text",
        'filename' : "nothing",
        'plaintext' : "CanTheyDoTheirFe"
    }
  (encrypted_blocks, padding_length, _, _) = encrypt("BUET CSE17 Batch", data)

  ascii_val = ""
  for block in encrypted_blocks:
    for col in block:
      print_spaced_hex_val(col)
    # print("")
    print("\nASCII value: ", end="")
    for col in block:
      ascii_val += ret_ASCII_val(col)
    print(ascii_val)