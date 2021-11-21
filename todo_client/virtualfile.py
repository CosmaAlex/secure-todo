import os
from Crypto.Cipher import AES

class VirtualFile:
    def __init__(self, filename, encrypt, key_filename=None, nonce_filename=None):
        self.filename = filename
        self.encrypt = encrypt
        encrypt_key = bytes()
        encrypt_nonce = bytes()

        if not os.path.exists(self.filename):
            raise Exception(self.filename + " does not exist")

        if self.encrypt:
            if not key_filename or not nonce_filename:
                raise Exception("You have to supply a key filename if encryption is enabled")

            if not os.path.exists(key_filename):
                raise Exception(key_filename + " does not exist")
            if not os.path.exists(nonce_filename):
                raise Exception(nonce_filename + " does not exist")

            with open(key_filename, "rb") as kf:
                encrypt_key = kf.read()
                kf.close()
            if len(encrypt_key) != 32:
                raise Exception("The key is not 256 bit long!")

            with open(nonce_filename, "rb") as nf:
                encrypt_nonce = nf.read()
                nf.close()
            if len(encrypt_nonce) != 8:
                raise Exception("The nonce is not 64 bit long!")

            self.cipher = AES.new(encrypt_key, AES.MODE_CTR, nonce=encrypt_nonce)
        

    def vread(self):
        content = bytes()
        with open(self.filename, "rb") as f:
            content = f.read()
            f.close()

        if not self.encrypt:
            return content
        else:
            return self.cipher.encrypt(content)

    def vwrite(self, content):
        with open(self.filename, "wb") as f:
            if not self.encrypt:
                f.write(content)
            else:
                f.write(self.cipher.decrypt(content))
            f.close()

    def vappend(self, content):
        with open(self.filename, "ab") as f:
            f.write("####### APPENDED #######")
            if not self.encrypt:
                f.write(content)
            else:
                f.write(self.cipher.decrypt(content))
            f.close()
