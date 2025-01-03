from gam_controller import GamController
import json
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--component', required=True, help='Name of the Business Component', dest='component')
    args = parser.parse_args()
    gc = GamController(args.component)
    
    print("====================================================")
    print("                 Component Config                   ")
    print("====================================================")
    print(json.dumps(json.loads(gc.component_config), indent=4))
    print()
    
    print("====================================================")
    print("                 Hydra Payload                      ")
    print("====================================================")
    print(json.dumps(json.loads(gc.hydra_payload), indent=4))
    print()

    
    # Post UMB Message
    response = gc.post_umb_message()
    if response:
        print("UMB Message Sent Sucessfully!")
    else:
        print("Request Failed!")

    print("Response:", response)
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)
