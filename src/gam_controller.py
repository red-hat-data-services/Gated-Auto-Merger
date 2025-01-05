from datetime import datetime
import json
import os
import ruamel.yaml
from hydra_adapter import HydraAdapter
import util

GAM_CONFIG = 'config/gam-config.yaml'
METADATA = 'data/metadata.yaml'
HYDRA_PAYLOAD_TEMPLATE = 'data/hydra_payload_template.json'

class GamController:
    def __init__(self, business_component: str, execution_id: str, gam_run_url: str):
        self.business_component = business_component
        self.gam_config = self.read_gam_config()
        self.component_config = self.read_component_config()
        self.execution_id = execution_id if execution_id else self.generate_execution_id()
        self.gam_run_url = gam_run_url
        self.execution_metadata = self.generate_execution_metadata()
        self.hydra_payload = self.generate_hydra_payload()

    def read_gam_config(self):
        return ruamel.yaml.YAML(typ='safe').load(open(GAM_CONFIG))
    
    def read_component_config(self):
        try:
            return [component for component in self.gam_config['components'] if component['name'] == self.business_component][0]
        except IndexError:
            raise ValueError(f"Component '{self.business_component}' not found in the configuration '{GAM_CONFIG}'.")

    def generate_execution_id(self):
        return datetime.now().strftime('%d%m%y%H%M%S%f')

    def generate_execution_metadata(self):
        metadata_path = "executions/" + self.component_config['name'] + "/" + self.execution_id
        
        # Initialize the execution metadata template
        execution_metadata_template = {
            'config': self.component_config,
            'metadata': {
                'git': None,
                'nvr': None,
                'execution_id': self.execution_id,
                'path': metadata_path,
                'gam_run_url': self.gam_run_url,
                'test_run_url': None,
                'test_result': None,
                'auto_merge_url': None,
                'status': None
            }
        }
        # Populate Execution Metadata Template
        execution_metadata = util.populate_execution_metadata(execution_metadata_template, self.component_config)

        # Save the updated metadata to the file
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.width = 500
        with open(METADATA, 'w') as metadata:
            yaml.dump(execution_metadata, metadata)

        return execution_metadata
    
    
    def generate_hydra_payload(self):
        payload = json.load(open(HYDRA_PAYLOAD_TEMPLATE))
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
