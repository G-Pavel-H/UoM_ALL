ciphertext = input("Input anything to encrypt ")
plaintext = ""
ciphertextPosition = 0

while (ciphertextPosition < len(ciphertext)):
    ciphertextChar = ciphertext[ciphertextPosition]
    ASCIIValue = ord(ciphertextChar)+3
    plaintext = plaintext + chr(ASCIIValue)
    ciphertextPosition += 1
print(plaintext)
