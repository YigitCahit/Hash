from hash import chain_hash_64

text=input("Enter text to hash: ")
hash=chain_hash_64(text)

print(f"Hash: {hash}")
