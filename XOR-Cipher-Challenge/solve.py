def find_key():
    print("--- XOR Key Recovery Tool ---")
    
    # Get the encrypted hex from the terminal
    hex_input = input("Enter the encrypted hex string: ").strip()
    
    # Get the known plaintext (e.g., ORDER:)
    plaintext_input = input("Enter the known header (plaintext): ")

    try:
        # Convert hex to bytes
        cipher_bytes = bytes.fromhex(hex_input)
        plain_bytes = plaintext_input.encode()

        recovered_key = ""
        
        # XOR the bytes to reveal the key
        for i in range(len(plain_bytes)):
            # XOR logic: Ciphertext ^ Plaintext = Key
            key_char = chr(cipher_bytes[i] ^ plain_bytes[i])
            recovered_key += key_char

        print(f"\n[+] Success! The recovered key is: {recovered_key}")
        
    except ValueError:
        print("\n[!] Error: Make sure you entered a valid Hex string (0-9, A-F).")

if __name__ == "__main__":
    find_key()