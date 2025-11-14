from typing import Union

MASK64 = (1 << 64) - 1

def rotl(x: int, r: int) -> int:
    r &= 63
    return ((x << r) & MASK64) | (x >> (64 - r))

CONST = [
    0x9E3779B97F4A7C15,
    0xC2B2AE3D27D4EB4F,
    0x165667B19E3779F9,
    0x85EBCA77C2B2AE63
]

def chain_hash_64(inp: Union[str, bytes]) -> str:
    if isinstance(inp, str):
        data = inp.encode("utf-8")
    else:
        data = bytes(inp)

    state = [
        0x243F6A8885A308D3 ^ CONST[0],
        0x13198A2E03707344 ^ CONST[1],
        0xA4093822299F31D0 ^ CONST[2],
        0x082EFA98EC4E6C89 ^ CONST[3],
    ]

    for b in data:
        state[0] = (state[0] ^ (b + CONST[0])) & MASK64
        state[1] = (state[1] + rotl(state[0], 13)) & MASK64
        state[2] = (state[2] ^ ((state[1] * CONST[1]) & MASK64)) & MASK64
        state[3] = (state[3] + rotl(state[2], 37)) & MASK64

        for i in range(4):
            a = state[i]
            bidx = (i + 1) & 3
            mixed = ((a ^ state[bidx]) * CONST[i]) & MASK64
            state[i] = rotl(mixed, (i * 17 + 7)) ^ ((mixed >> (i + 3)) & MASK64)
            
    length = len(data)
    state[0] = (state[0] ^ (length * 0x9E3779B97F4A7C15)) & MASK64
    state[1] = (state[1] + rotl(state[0], 23)) & MASK64
    state[2] = (state[2] ^ rotl(state[1], 41)) & MASK64
    state[3] = (state[3] + ((state[2] * 0x2545F4914F6CDD1D) & MASK64)) & MASK64

    for round in range(16):
        state[0] = (state[0] ^ (rotl(state[3], 31) + (state[1] * CONST[0] & MASK64))) & MASK64
        state[1] = (state[1] + (rotl(state[0], 27) ^ (state[2] * CONST[1] & MASK64))) & MASK64
        state[2] = (state[2] ^ (rotl(state[1], 17) + (state[3] * CONST[2] & MASK64))) & MASK64
        state[3] = (state[3] + (rotl(state[2], 41) ^ (state[0] * CONST[3] & MASK64))) & MASK64

        state[0], state[1], state[2], state[3] = state[3], rotl(state[0], 19), state[1] ^ state[2], rotl(state[3], 11)

    out_bytes = b""
    for v in state:
        out_bytes += v.to_bytes(8, "big")

    return out_bytes.hex()
