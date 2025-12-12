# Monkey patch file for things we override in the models
import base64
import json

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.exceptions import CryptoError

from .params_api import ParamsApi


class SecureData:
    def __init__(self):
        self.Key = None
        self.Nonce = None
        self.Payload = None

    def seal(self, server_side_pubkey: bytes, data: str) -> None:
        try:
            # Generate ephemeral key pair
            our_private_key = PrivateKey.generate()
            our_public_key = our_private_key.public_key

            # Store the ephemeral public key
            self.Key = bytes(our_public_key)
            self.Key = base64.b64encode(self.Key).decode("utf-8")

            # Generate a nonce
            nonce = nacl.utils.random(Box.NONCE_SIZE)
            self.Nonce = nonce
            self.Nonce = base64.b64encode(self.Nonce).decode("utf-8")

            # Encrypt the data
            box = Box(our_private_key, PublicKey(server_side_pubkey))
            data = json.dumps(data).encode('utf-8')
            self.Payload = box.encrypt(data, nonce).ciphertext
            self.Payload = base64.b64encode(self.Payload).decode("utf8")
        except CryptoError as e:
            raise Exception(f"Error encrypting data: {e}")


def custom_post_machine_param(cls, inst, body, uuid, key, **kwargs):
    # check if "key" is a secure param on the drp server
    param_api = ParamsApi(inst.api_client)
    param = param_api.get_param(key, **kwargs)
    if param.secure:
        # Example usage
        secure_data = SecureData()
        # Example peer public key (32 bytes)
        server_side_pubkey = inst.get_machine_pub_key(uuid, **kwargs)
        server_side_pubkey = base64.b64decode(server_side_pubkey)
        # Data to encrypt
        data = body
        # Seal the data
        secure_data.seal(server_side_pubkey, data)
        body = {"Key": f"{secure_data.Key}",
                "Nonce": f"{secure_data.Nonce}",
                "Payload": f"{secure_data.Payload}"}
        # finally fall back into the main call being made
    inst.post_machine_param_with_http_info(body, uuid, key, **kwargs)
