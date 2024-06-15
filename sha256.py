import struct

def right_rotate32(n, d):
    return (n >> d) | (n << (32 - d)) & 0xFFFFFFFF

def C0(word):
    return right_rotate32(word, 7) ^ right_rotate32(word, 18) ^ (word >> 3)

def C1(word):
    return right_rotate32(word, 17) ^ right_rotate32(word, 19) ^ (word >> 10)

def sum0(a):
    return right_rotate32(a, 2) ^ right_rotate32(a, 13) ^ right_rotate32(a, 22)

def sum1(e):
    return right_rotate32(e, 6) ^ right_rotate32(e, 11) ^ right_rotate32(e, 25)

def choice(e, f, g):
    return (e & f) ^ ((~e) & g)

def majority(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)

def expension_block(block):
    for i in range(16, 64):
        block[i] = (block[i - 16] + C0(block[i - 15]) + block[i - 7] + C1(block[i - 2])) & 0xFFFFFFFF

def compress(w, H):
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    a, b, c, d, e, f, g, h = H

    for i in range(64):
        temp1 = (h + sum1(e) + choice(e, f, g) + K[i] + w[i]) & 0xFFFFFFFF
        temp2 = (sum0(a) + majority(a, b, c)) & 0xFFFFFFFF
        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF

    H[0] = (H[0] + a) & 0xFFFFFFFF
    H[1] = (H[1] + b) & 0xFFFFFFFF
    H[2] = (H[2] + c) & 0xFFFFFFFF
    H[3] = (H[3] + d) & 0xFFFFFFFF
    H[4] = (H[4] + e) & 0xFFFFFFFF
    H[5] = (H[5] + f) & 0xFFFFFFFF
    H[6] = (H[6] + g) & 0xFFFFFFFF
    H[7] = (H[7] + h) & 0xFFFFFFFF

def create_blocks(message):
    lenstr = len(message)
    field_len = 8
    bitstr = lenstr * 8
    payload = lenstr + field_len
    padding = (64 - (payload % 64)) % 64
    block_count = (payload + padding) // 64

    byte_message = bytearray(message, 'utf-8')
    byte_message += b'\x80'
    padding_len = padding - 1
    byte_message += b'\x00' * padding_len
    byte_message += bitstr.to_bytes(8, byteorder='big')

    blocks = [[0] * 64 for _ in range(block_count)]
    for i in range(block_count):
        for j in range(64):
            blocks[i][j] = byte_message[i * 64 + j]
    return blocks

def hash_message(message):
    h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    blocks = create_blocks(message)

    for block in blocks:
        w = [0] * 64
        for i in range(16):
            w[i] = struct.unpack('>I', bytes(block[i * 4:(i + 1) * 4]))[0]
        expension_block(w)
        compress(w, h)

    return h

message = "hello world"
hashed = hash_message(message)
print('Хэш сообщения:', ''.join(f'{x:08x}' for x in hashed))