from gam_controller import GamController
import json
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--component', required=True, help='Name of the Business Component', dest='component')
    parser.add_argument('--execution_id', required=False, help='A Unique ID for The GAM Execution', dest='execution_id')
    parser.add_argument('--gam_run_url', required=False, help='Github Action Job run URL for GAM', dest='gam_run_url')
    args = parser.parse_args()
    
    gc = GamController(args.component, args.execution_id, args.gam_run_url)
    print("====================================================")
    print("                 Component Config                   ")
    print("====================================================")
    print(json.dumps(gc.component_config, indent=4))
    print()
    print("====================================================")
    print("                 Hydra Payload                      ")
    print("====================================================")
    print(json.dumps(gc.hydra_payload, indent=4))
    print()

    
    # Post UMB Message
    response = gc.post_umb_message()
    
    # Print response details
    print("Response:", response)
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)

    # Check if the response was successful (status code 2xx)
    if response.ok:
        print("UMB Message Sent Successfully!")
    else:
        print("Request Failed!")
        sys.exit(1)  # Exit the program with a non-zero status code to indicate failure
