def encode(text: str, key: str) -> str:
    """
        Encode text using Vigenère cipher
    """
    encodedText = []

    for i in range(len(text)):
        keyC = key[i % len(key)]
        textC = text[i]
        encodedText.append(chr(ord(textC) + ord(keyC)))
    
    return "".join(encodedText)

def decode(encodedText: str, key: str) -> str:
    """
        Decode text
    """
    decodedText = []

    for i in range(len(encodedText)):
        keyC = key[i % len(key)]
        textC = encodedText[i]
        decodedText.append(chr(ord(textC) - ord(keyC)))
    
    return "".join(decodedText)