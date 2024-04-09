import signal
import requests
import sys
import os
import json
import afl

base_url = 'http://127.0.0.1:8000/'

def main(a):

    endpoint_url = a

    url = base_url + endpoint_url

    # Define the headers with cookies
    headers = {
        'Cookie': 'csrftoken=jr6DahhKuGKgXX6Dxb3F4iR9FgiiQkAL; sessionid=bvlvh8bqcwhbzr2eqqk3blv9x5b68q4r'
    }

    try:
        # Send a GET request with the defined headers and cookies
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful!")
            # Process the response data as needed
            print("Response:")
            print(response.text)
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    
    

if __name__ == '__main__':
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # this should have no effect on the forkserver
    afl.init()
    
    a = sys.stdin.read()
    
    main(a)
    os._exit(0)