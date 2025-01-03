from gam_controller import GamController
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--component', required=True, help='Name of the Business Component', dest='component')
    args = parser.parse_args()
    gc = GamController(args.component)
    
    print("====================================================")
    print("                 Component Config                   ")
    print("====================================================")
    print(gc.component_config)
    print()
    
    print("====================================================")
    print("                 Hydra Payload                      ")
    print("====================================================")
    print(gc.hydra_payload)
    print()

    
    # Post UMB Message
    response = gc.post_umb_message()
    if response:
        print("UMB Message Sent Sucessfully!")
    else:
        print("Request Failed!")

    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)
