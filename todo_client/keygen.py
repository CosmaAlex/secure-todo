from Crypto.Random import get_random_bytes

# generate 256 bit key
print("Generating random key")
key = get_random_bytes(32)

print("Writing to file .key")
with open(".key", "wb") as f:
    f.write(key)
    f.close()

# generate 64 bit nonce
print("Generating random nonce")
nonce = get_random_bytes(8)

print("Writing to file .nonce")
with open(".nonce", "wb") as f:
    f.write(nonce)
    f.close()

print("Done")
