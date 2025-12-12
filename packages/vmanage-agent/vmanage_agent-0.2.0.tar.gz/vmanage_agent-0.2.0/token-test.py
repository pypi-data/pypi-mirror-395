from cryptography.fernet import Fernet


def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    return key.decode()


def encrypt_message(message, key):
    """
    Encrypts a message
    """
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message


def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()


dict_encrypt = {
    "master_finger": "49:e4:7d:52:fc:27:cb:3b:ee:f1:82:b2:ee:50:08:ff:27:84:3d:5a:2c:03:5c:66:7d:a7:f7:0e:3c:22:54:66",
    "master_address": "143.244.167.225",
}

# secret = generate_key()
# print(secret)
# encrypted_text = encrypt_message(json.dumps(dict_encrypt), secret)
# print(encrypted_text)
# print(decrypt_message(encrypted_text, secret))
