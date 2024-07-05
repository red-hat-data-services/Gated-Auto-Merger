import json

import yaml
from datetime import datetime
from hydra_adapter import hydra_adapter
import os
# generate execution id and update to metadata branch

__GAM_CONFIG__ = 'config/gam-config.yaml'
class gam_controller:
    def __init__(self, business_component:str):
        self.business_component = business_component
        self.gam_config = self.read_gam_config()
        self.component_config = self.read_component_config()
        self.execution_id = self.generate_execution_id()
        self.execution_metadata = self.generate_execution_metadata()


    def read_component_config(self):
        return [component for component in self.gam_config['config']['components'] if component['name'] == self.business_component][0]

    def read_gam_config(self):
        return yaml.load(open(__GAM_CONFIG__), Loader=yaml.SafeLoader)

    def generate_execution_id(self):
        return datetime.now().strftime('%d%m%y%H%M%S%f')

    def generate_execution_metadata(self):
        meta = self.component_config
        meta['execution_id'] = self.execution_id
        return meta

    def post_umb_message(self):
        try:
            hydra = hydra_adapter()
            print(os.getcwd())
            url = "https://api.enterprise.redhat.com/hydra/umb-bridge/v1/publish"
            payload = json.load(open('data/umb_payload_template.json'))
            payload['gam'] |= self.component_config
            payload['gam']['execution_id'] = self.execution_id
            print('hydra payload ', payload)
            payload = json.dumps(payload)
            secret_token = os.getenv('HYDRA_TOKEN')  # Retrieve secret token from environment variable
            if secret_token is None:
                raise ValueError("Secret token not found in environment variables.")

            signature = hydra.generate_signature(payload, secret_token)
            print("Generated Signature:", signature)

            response = hydra.send_post_request(url, payload, signature)
            if response:
                print("Request Successful!")
            else:
                print("Request Failed!")

            print("Response Status Code:", response.status_code)
            print("Response Body:", response.text)

        except Exception as e:
            print("Error:", e)
