import hmac
import hashlib
import requests

HYDRA_BRIDGE_URL = "https://api.enterprise.redhat.com/hydra/umb-bridge/v1/publish"

"""
https://github.com/riprasad/hydra-github-umb-bridge
"""
class HydraAdapter:
    def __init__(self, payload, hydra_token):
        self.payload = payload
        self.hydra_token = hydra_token
        self.signature = self.generate_signature()


    def generate_signature(self):
        # Encode payload and secret_token as bytes
        payload_bytes = self.payload.encode('utf-8')
        hydra_token_bytes = self.hydra_token.encode('utf-8')

        # Create HMAC SHA256 signature
        hmac_obj = hmac.new(hydra_token_bytes, msg=payload_bytes, digestmod=hashlib.sha256)
        signature = "sha256=" + hmac_obj.hexdigest()
        return signature


    def post_umb_message(self):
        headers = {
            'Content-Type': 'application/json',
            'X-GitHub-Event': 'custom',
            'X-Hub-Signature-256': self.signature
        }

        response = requests.post(HYDRA_BRIDGE_URL, headers=headers, data=self.payload)
        return response
