def xor_encrypt(data, key):
    key_bytes = key.encode()
    result = bytearray()

    for i in range(len(data)):
        result.append(data[i] ^ key_bytes[i % len(key_bytes)])

    return bytes(result)