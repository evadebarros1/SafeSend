from cryptography.fernet import Fernet
import argparse

def generate_key(path = "key.key"):
    key = Fernet.generate_key()
    with open(path,"wb") as f:
        f.write(key)
    print(f"[+] Key saved to {path} ")
    return key

def load_key(path):
    return open(path,"rb").read()

def encrypt_file(filepath,key):
    fernet = Fernet(key)
    with open(filepath, "rb") as plaintxt:
        f = plaintxt.read()

    encrypted_file = fernet.encrypt(f)
    with open(filepath + ".enc", "wb") as f:
        f.write(encrypted_file)
    
    print("The plaintext has been encrypted")
    return filepath + ".enc"

def decrypt_cipher(filepath,key):
    fernet = Fernet(key)
    with open(filepath,"rb") as f:
        output = f.read()
    decrypted = fernet.decrypt(output)
    output_path = filepath.replace(".enc","_decrypted")
    with open(output_path,"wb") as f:
        f.write(decrypted)
    print("The ciphertext has been decrypted")
    return output_path

def cli_in_out():
    parser = argparse.ArgumentParser(description="SafeSend: Encrypt/Decrypt files")
    subparsers = parser.add_subparsers(dest="command")

    parser_key_gen = subparsers.add_parser("generate-key")
    parser_key_gen.add_argument("--key",default="key.key",help = "Path to save key")

    args = parser.parse_args()

    if args.command == "generate-key":
        generate_key(args.key)

def main():
    cli_in_out()
    # filepath = "test_plain.txt"
    # key = generate_key()
    # filepath = encrypt_file(filepath,key)
    # output_path = decrypt_cipher(filepath,key)
main()