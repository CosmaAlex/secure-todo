from Crypto.Random import get_random_bytes

# generate 256 bit key
print("Generating random key")
key = get_random_bytes(32)

print("Writing to file")
with open(".key", "wb") as f:
    f.write(key)
    f.close()

print("Done")
