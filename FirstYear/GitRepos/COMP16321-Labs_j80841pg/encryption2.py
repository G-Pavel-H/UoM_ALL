plaintext = input("Input anything to encrypt ")
ciphertext = ""
plaintextPosition = 0

while (plaintextPosition < len(plaintext)):
    plaintextChar = plaintext[plaintextPosition]
    ASCIIValue = ord(plaintextChar)-3
    ciphertext = ciphertext + chr(ASCIIValue)
    plaintextPosition += 1
print(ciphertext)
