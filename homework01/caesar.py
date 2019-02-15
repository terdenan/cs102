def next_symbol(symbol):

    if ("A" <= symbol and symbol <= "Z"):
        return chr(ord("A") + (ord(symbol) - ord("A") + 3) % 26)
    else:
        return chr(ord("a") + (ord(symbol) - ord("a") + 3) % 26)


def prev_symbol(symbol):

    if ("A" <= symbol and symbol <= "Z"):
        return chr(ord("A") + (26 + ord(symbol) - ord("A") - 3) % 26)
    else:
        return chr(ord("a") + (26 + ord(symbol) - ord("a") - 3) % 26)


def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("sillyError")
    ''
    """
    ciphertext = ""

    for i in plaintext:
        ciphertext += next_symbol(i)

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    for i in ciphertext:
        plaintext += prev_symbol(i)

    return plaintext
