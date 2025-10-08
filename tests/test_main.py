import os
import pytest
from cryptography.fernet import InvalidToken
from safesend import generate_key, encrypt_file, decrypt_cipher

TEST_KEY_PATH = "tests/test_key.key"
TEST_FILE_PATH = "tests/test_file.txt"
TEST_ENC_PATH = "tests/test_file.txt.enc"
TEST_DEC_PATH = "tests/test_file.txt.dec"

@pytest.fixture(scope="function",autouse=True)
def cleanup_files():
    "Clean files up before and after testing"
    yield
    for file in os.listdir("tests"):
        path = os.path.join("tests", file)
        if os.path.isfile(path) and file.endswith((".txt", ".key", ".enc", ".dec")):
            os.remove(path)

def test_generate_key_create_file():
    key = generate_key(TEST_KEY_PATH)
    assert os.path.exists(TEST_KEY_PATH)
    assert len(key) > 0

def test_encrypt_decrypt_file():
    #Create plaintext file
    data = b"This is plain text data to be sent securely"
    with open(TEST_FILE_PATH,"wb") as f:
        f.write(data)
    
    #genreeate a key and encrypt the file
    key = generate_key(TEST_KEY_PATH)
    encrypted_filepath = encrypt_file(TEST_FILE_PATH,TEST_KEY_PATH)

    #decrypt the ciphered text
    decrypt_cipherpath = decrypt_cipher(encrypted_filepath,TEST_KEY_PATH)
    with open(decrypt_cipherpath, "rb") as f: 
        decrypt_ciphertext = f.read()
    assert decrypt_ciphertext == data

def test_decrypt_wrong_key_raise_error():
    data = b"Special secret message"
    with open(TEST_FILE_PATH,"wb") as f:
        f.write(data)

    #valid key for encryption
    generate_key(TEST_KEY_PATH)
    encrypt_file(TEST_FILE_PATH,TEST_KEY_PATH)

    #invalid key for decryption
    invalid_key_path = "tests/made_up_key.key"
    generate_key(invalid_key_path)
    with pytest.raises(InvalidToken):
        decrypt_cipher(TEST_ENC_PATH,invalid_key_path)