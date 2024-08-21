from gam_controller import gam_controller
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--component', required=True, help='Name of the Business Component', dest='component')
    args = parser.parse_args()
    gc = gam_controller(args.component)
    print(gc.component_config)
    gc.post_umb_message()
