import yaml
from datetime import datetime

# components = yaml.load(open('../config/components.yaml'), Loader=yaml.SafeLoader)
# print(components)

print(datetime.now().strftime('%d%m%y%H%M%S%f'))