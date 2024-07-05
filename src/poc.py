import yaml
from datetime import datetime

components = yaml.load(open('../config/gam-config.yaml'), Loader=yaml.SafeLoader)
components = {'name': 'Dashboard', 'cpaas_repos': ['odh-dashboard'], 'non_cpaas_repos': [], 'robot_tags': 'Dashboard', 'Test_Platform': 'Jenkins', 'Jenkins_Job': '', 'execution_id': '050724130415305145'}
print(components)
print(yaml.dump({'metadata': components}))
print(datetime.now().strftime('%d%m%y%H%M%S%f'))