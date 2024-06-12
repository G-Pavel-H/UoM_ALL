plaintext = input("Input a text to encrypt ")
plaintext = plaintext.upper() #upper is used for lowercase inputs
ciphertext = ""
alphabet = "XYZABCDEFGHIJKLMNOPQRSTUVWXYZABC"
plaintextPosition = 0

while (plaintextPosition < len(plaintext)):
    plaintextChar = plaintext[plaintextPosition]
    alphabetPosition = 3
    while plaintextChar != alphabet[alphabetPosition]:
        alphabetPosition +=1
    alphabetPosition = alphabetPosition - 3
    ciphertext = ciphertext + alphabet[alphabetPosition]
    plaintextPosition += 1
print(ciphertext)
