from gam_controller import gam_controller
import argparse

if __name__ == '__main__':
    gc = gam_controller('Dashboard')
    print(gc.component_config)
    gc.post_umb_message()