import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class VirtualFile:
    def __init__(self, filename, encrypt, key_filename=None):
        self.filename = filename
        self.encrypt = encrypt
        self.encrypt_key = bytes()
        self.mac_len = 16           # MAC length constant
        self.nonce_len = 16         # Nonce length constant

        if not os.path.exists(self.filename):
            raise Exception(self.filename + " does not exist")

        if self.encrypt:
            if not key_filename:
                raise Exception("You have to supply a key filename if encryption is enabled")

            if not os.path.exists(key_filename):
                raise Exception(key_filename + " does not exist")

            with open(key_filename, "rb") as kf:
                self.encrypt_key = kf.read()
                kf.close()
            if len(self.encrypt_key) != 32:
                raise Exception("The key is not 256 bit long!")


    def vread(self):
        content = bytes()
        with open(self.filename, "rb") as f:
            content = f.read()
            f.close()

        if not self.encrypt:
            return content
        else:
            nonce = get_random_bytes(self.nonce_len)
            cipher = AES.new(self.encrypt_key, AES.MODE_EAX, nonce=nonce, mac_len=self.mac_len)
            ciphertext, tag = cipher.encrypt_and_digest(content)
            return nonce + tag + ciphertext

    def vwrite(self, content):
        with open(self.filename, "wb") as f:
            if not self.encrypt:
                f.write(content)
            else:
                try:
                    plaintext = self.__decrypt(content)
                except (ValueError, KeyError) as e:
                    print("Error in decryption!")
                    return -1;
                f.write(plaintext)
            f.close()
        return 0;

    def __decrypt(self, content):
        nonce = content[:self.nonce_len]
        tag = content[self.nonce_len:self.nonce_len+self.mac_len]
        ciphertext = content[self.nonce_len+self.mac_len:]
        cipher = AES.new(self.encrypt_key, AES.MODE_EAX, nonce=nonce, mac_len=self.mac_len)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext


    def vappend(self, content):
        with open(self.filename, "ab") as f:
            f.write("####### APPENDED #######")
            if not self.encrypt:
                f.write(content)
            else:
                try:
                    plaintext = self.__decrypt(content)
                except (ValueError, KeyError) as e:
                    print("Error in decryption!")
                    return -1;
                f.write(plaintext)
            f.close()
        return 0;
