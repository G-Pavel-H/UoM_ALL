ciphertext = input("Input a ciphertext to decrypt ")
ciphertext = ciphertext.upper() #upper is used so that even if lower case is inputted everything workes correctly
plaintext = ""
alphabet = "XYZABCDEFGHIJKLMNOPQRSTUVWXYZABC"
ciphertextPosition = 0

while (ciphertextPosition < len(ciphertext)):
    ciphertextChar = ciphertext[ciphertextPosition]
    alphabetPosition = 3
    while ciphertextChar != alphabet[alphabetPosition]:
        alphabetPosition += 1
    alphabetPosition = alphabetPosition + 3
    plaintext = plaintext + alphabet[alphabetPosition]
    ciphertextPosition += 1
print(plaintext)
