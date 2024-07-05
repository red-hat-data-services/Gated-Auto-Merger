import yaml
from datetime import datetime

components = yaml.load(open('../config/gam-config.yaml'), Loader=yaml.SafeLoader)
print(components)
print(yaml.dump(components))
print(datetime.now().strftime('%d%m%y%H%M%S%f'))