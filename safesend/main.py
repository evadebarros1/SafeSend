from cryptography.fernet import Fernet
import argparse

def generate_key(path = "keys/key.key"):
    key = Fernet.generate_key()
    with open(path,"wb") as f:
        f.write(key)
    print(f"[+] Key saved to {path} ")
    return key

def load_key(path):
    return open(path,"rb").read()

def encrypt_file(filepath,key_path="keys/key.key"):
    key = open(key_path,"rb").read()
    fernet = Fernet(key)
    with open(filepath, "rb") as plaintxt:
        f = plaintxt.read()

    encrypted_file = fernet.encrypt(f)
    with open(filepath + ".enc", "wb") as f:
        f.write(encrypted_file)
    
    print("The plaintext has been encrypted")
    return filepath + ".enc"

def decrypt_cipher(filepath,key_path="keys/key.key"):
    key = open(key_path,"rb").read()
    fernet = Fernet(key)
    with open(filepath, "rb") as cipher:
        f = cipher.read()
    decrypted = fernet.decrypt(f)
    output_path = filepath.replace(".enc",".dec")
    with open(output_path,"wb") as f:
        f.write(decrypted)
    print("The ciphertext has been decrypted")
    return output_path

def cli_in_out():
    parser = argparse.ArgumentParser(description="SafeSend: Encrypt/Decrypt files")
    subparsers = parser.add_subparsers(dest="command")

    #Generate a key
    parser_key_gen = subparsers.add_parser("generate-key")
    parser_key_gen.add_argument("--key",default="keys/key.key",help = "Path to save key. Default location used if not specified")

    #Encrypt a file
    parser_encrypt = subparsers.add_parser("encrypt-file")
    parser_encrypt.add_argument("file",help = "File to be encrypted")
    parser_encrypt.add_argument("--key",default="keys/key.key",help = "Path to save key. Default location used if not specified")

    #Decrypt a file
    parser_decrypt = subparsers.add_parser("decrypt-file")
    parser_decrypt.add_argument("file",help = "File to be decrypted")
    parser_decrypt.add_argument("--key",default="keys/key.key",help = "Path to save key. Default location used if not specified")

    args = parser.parse_args()

    if args.command == "generate-key":
        generate_key(args.key)
    if args.command == "encrypt-file":
        encrypt_file(args.file,args.key)
    if args.command == "decrypt-file":
        decrypt_cipher(args.file,args.key)
    else:
        parser.print_help()

def main():
    cli_in_out()

if __name__ == "__main__":
    main()