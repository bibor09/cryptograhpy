import array

def encrypt(input, key_stream_generator_alg, k):
    key = key_stream_generator_alg(len(input), k)
    byte_stream = array.array('b', input.encode())
    
    encoded_stream = [byte_stream[i]^key[i] for i in range(len(byte_stream))]
    return bytes(encoded_stream)

def decrypt(input, key_stream_generator_alg, k):
    byte_stream = input
    key = key_stream_generator_alg(len(byte_stream), k)

    decoded_stream = [byte_stream[i]^key[i] for i in range(len(byte_stream))]
    return bytes(decoded_stream).decode()