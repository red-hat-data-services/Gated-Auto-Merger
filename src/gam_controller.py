import json

import yaml
from datetime import datetime
from hydra_adapter import HydraAdapter
import os

GAM_CONFIG = 'config/gam-config.yaml'
METADATA = 'data/metadata.yaml'
UMB_PAYLOAD_TEMPLATE = 'data/umb_payload_template.json'

class GamController:
    def __init__(self, business_component:str):
        self.business_component = business_component
        self.gam_config = self.read_gam_config()
        self.component_config = self.read_component_config()
        self.execution_id = self.generate_execution_id()
        self.execution_metadata = self.generate_execution_metadata()
        self.hydra_payload = self.generate_hydra_payload()

    def read_gam_config(self):
        return yaml.load(open(GAM_CONFIG), Loader=yaml.SafeLoader)
    
    def read_component_config(self):
        try:
            return [component for component in self.gam_config['components'] if component['name'] == self.business_component][0]
        except IndexError:
            raise ValueError(f"Component '{self.business_component}' not found in the configuration '{GAM_CONFIG}'.")

    def generate_execution_id(self):
        return datetime.now().strftime('%d%m%y%H%M%S%f')

    def generate_execution_metadata(self):
        execution_metadata = {
            'config': self.component_config,
            'metadata': {
                'execution_id': self.execution_id,
                'job_run_url': None ,
                'result': None
                
            }
        }
        with open(METADATA, 'w') as metadata:
            metadata.write(yaml.dump(execution_metadata))
        return execution_metadata
    
    def generate_hydra_payload(self):
        payload = json.load(open(UMB_PAYLOAD_TEMPLATE))
        payload['gam'] |= self.execution_metadata
        return payload

    def post_umb_message(self):
        try:
            # Retrieve secret token from environment variable
            hydra_token = os.getenv('HYDRA_TOKEN') 
            if hydra_token is None:
                raise ValueError("Secret token not found in environment variables.")

            payload = json.dumps(self.hydra_payload)
            hydra = HydraAdapter(payload, hydra_token)
            return hydra.post_umb_message()

        except Exception as e:
            print("Error: Unable to post UMB message.")
            print("Error:", e)
