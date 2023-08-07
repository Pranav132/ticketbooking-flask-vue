import secrets
key = secrets.token_hex(32)  # 32 bytes * 8 bits/byte = 256 bits
print(key)
