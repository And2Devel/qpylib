# Copyright 2019 IBM Corporation All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

import base64
import string
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Enginev4():
    ''' Enginev4 uses Fernet encryption.
        See https://cryptography.io/en/latest/fernet.
    '''
    def __init__(self, config, app_uuid):
        self.version = 4
        self.config = config
        self.app_uuid = app_uuid

    def encrypt(self, clear_text_string):
        fernet = Fernet(self._derive_key())
        encrypted_bytes = fernet.encrypt(clear_text_string.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')

    def decrypt(self):
        fernet = Fernet(self._derive_key())
        decrypted_bytes = fernet.decrypt(self.config['secret'].encode('utf-8'))
        return decrypted_bytes.decode('utf-8')

    def _derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.config['salt'].encode('utf-8'),
            iterations=self.config['iterations'],
            backend=default_backend()
        )
        key = kdf.derive(self.app_uuid.encode('utf-8'))
        return base64.urlsafe_b64encode(key)

    @staticmethod
    def generate_config():
        characters = string.ascii_letters + string.digits + string.punctuation
        salt = ''.join(secrets.choice(characters) for _ in range(16))
        return {'version': 4, 'salt': salt, 'iterations': 100000}
