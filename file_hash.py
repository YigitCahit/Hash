from hash import chain_hash_64

file_path = input("Enter file path: ")

try:
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    hash_value = chain_hash_64(file_data)
    print(f"File Hash: {hash_value}")
    
except FileNotFoundError:
    print("File not found!")
except Exception as e:
    print(f"Error: {e}")
