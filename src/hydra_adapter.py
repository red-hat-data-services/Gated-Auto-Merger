import os
import hmac
import hashlib
import requests

class hydra_adapter:
    def __init__(self):
        pass


    def generate_signature(self, payload, secret_token):
        # Encode payload and secret_token as bytes
        payload_bytes = payload.encode('utf-8')
        secret_token_bytes = secret_token.encode('utf-8')

        # Create HMAC SHA256 signature
        hmac_obj = hmac.new(secret_token_bytes, msg=payload_bytes, digestmod=hashlib.sha256)
        signature = "sha256=" + hmac_obj.hexdigest()
        return signature


    def send_post_request(self, url, payload, signature):
        headers = {
            'Content-Type': 'application/json',
            'X-GitHub-Event': 'custom',
            'X-Hub-Signature-256': signature
        }

        print("Sending POST Request....")
        response = requests.post(url, headers=headers, data=payload)
        return response
