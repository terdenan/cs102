def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    def next_symbol(symbol, keysymbol):

        shift = 0

        if ("A" <= keysymbol and keysymbol <= "Z"):
            shift = ord(keysymbol) - ord('A')
        else:
            shift = ord(keysymbol) - ord('a')

        if ("A" <= symbol and symbol <= "Z"):
            return chr(ord("A") + (ord(symbol) - ord("A") + shift) % 26)
        else:
            return chr(ord("a") + (ord(symbol) - ord("a") + shift) % 26)

    ciphertext = ""

    for i in range(len(plaintext)):
        ciphertext += next_symbol(plaintext[i], keyword[i % len(keyword)])
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    def next_symbol(symbol, keysymbol):

        shift = 0

        if ("A" <= keysymbol and keysymbol <= "Z"):
            shift = ord(keysymbol) - ord('A')
        else:
            shift = ord(keysymbol) - ord('a')

        if ("A" <= symbol and symbol <= "Z"):
            return chr(ord("A") + (26 + ord(symbol) - ord("A") - shift) % 26)
        else:
            return chr(ord("a") + (26 + ord(symbol) - ord("a") - shift) % 26)

    plaintext = ""

    for i in range(len(ciphertext)):
        plaintext += next_symbol(ciphertext[i], keyword[i % len(keyword)])
    return plaintext
