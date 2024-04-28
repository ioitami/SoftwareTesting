import signal
import requests
import sys
import os
import json
import random
import afl


def main(input):
    base_url = 'http://127.0.0.1:8000/'
    
    # IF FUZZED INPUT IS "GET"
    if(input[0] == "GET"):
        url = ''
        endpoint_url = ''
         
        if(input[1] != ""):
            endpoint_url = input[1]
        
        if(input[2] != ""):
            endpoint_url += input[2]

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
                # print("Response:")
                # print(response.text)
            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            
    # IF FUZZED INPUT IS "POST"
    if(input[0] == "POST"):
        
        if(input[1] != ""):
            endpoint_url = input[1]

        url = base_url + endpoint_url

        if(input[2] != ""):
            random_name = input[2]
            random_info = input[2]
            random_price = input[2]
        else:
            random_name = ""
            random_info = ""
            random_price = ""

        # Define the form data with random values
        form_data = {
            'name': random_name,
            'info': random_info,
            'price': random_price
        }

        # Define the headers with cookies
        headers = {
            'Cookie': 'csrftoken=5vvs6151ScRQGpdMlKAf8FAFERO67MmK; sessionid=c35o5m7xkymbjdtcu9k916f8jfj2f8x7', # Optional
        }

        try:
            print(json.dumps(form_data))
            response = requests.post(url, headers=headers, data=json.dumps(form_data))

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                print("Request successful!")
                # Process the response data as needed
                # print("Response:")
                # print(response.text)

            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            
    if(input[0] == "PUT"):
        base_url = 'http://127.0.0.1:8000/'

        endpoint_url = input[1]

        url = base_url + endpoint_url
        
        # Generate random values for the input fields
        random_value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        
        key = input[2]
        value = random_value

        headers = {
            'Cookie': 'csrftoken=5vvs6151ScRQGpdMlKAf8FAFERO67MmK; sessionid=c35o5m7xkymbjdtcu9k916f8jfj2f8x7', # Optional
        }
        
        try:
            # Check if the request was successful (status code 200)
            #response = requests.post(url, headers=headers, data=json.dumps(form_data))
            response = requests.put(url, headers=headers, data ={key:value})
            
            if response.status_code == 200:
                print("Request successful!")
                # Process the response data as needed
                # print("Response:")
                # print(response.text)

            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            
    # os._exit(0)
    
    

if __name__ == '__main__':
    # afl.init()
    # a = sys.stdin.read()
    b = [#ORI
        "GET,¬abc",
        "GET,,ábc",
        "POST,áccounts/login/,abcde",
        "POST,accounts/login/¬abcde",
        "POST,",
        "PUT,áccounts/login/,e",
        "PUT,accounts/login/,å",
        "偕听慣捯畮 ⽲穧穳瑥爯ⱡ抚摥",
        "GET,¬ab#",
        "GET,#ábc",
        "GET,%ábc",
        "GET,%abã",
        "GET,%aJã",
        "GET,?áb#",
        "POST,áccs/login%4abc",
        "PUT,/a%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%POST,%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%<%%-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/%%%%%%%%%%%%%%%ÿ%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%G%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%?%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%<%%-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%ccou%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%<%%-%%%%%%%%%%%%%%%%%%/%%%%%%%%%%%%%%ÿ%%%%%€ %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%G%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%6%%%%%%%%%%%d %%%%%%%%/%%%%%%%%%%%%%%%ÿ%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%G%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%6%%%%%%%%%%%d %%%%%%%%%%%%%%%%%%%%%Fbc",
        "PUT,/ccouYtUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU UUUUUhUUioginUUUUUUUUUUab#dUUUUUUUUUUUUUUUUUUUUUU,%ccouUUUiUUUcUUUUUUUUUUUUUUUUUUccouUUUUUUUUUUUUUUUUUUUUUiUUUUUUUUUUUUUUUUUUUUUUUUUUaUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU¬UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUvUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUoUUUUUUUUUUUUUUUUUUUUUUUUUUUú  úUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUKUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUKUUUUUUUUUUU UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU UUUUUUUUUUUnUUUUUUUUUs/login/, ",
        "GET,¬abc",
        "GET,,ábc",
        "PUT,äatatb/product/,DVtaCp",
        "PUT,datatb/product/,ÄVtaCp",
        "POST,áccounts/login/,abcde",
        "POST,accounts/login/¬abcde",
        "GET,¬ab#",
        "GET,#ábc",
        "GET,%ábc",
        "GET,%abã",
        "PUT,äatatb%product/,Cp",
        "PUT,datatb%product/,Ãp",
        "PUT,datatb;pct/,Ãp",
        "PUT,datatb;pct,ìCp"
        "PUT,	ÿ?",
        "POST,",
        "GET,?áb#", 
        "PUT,äatatb/product%4DVta",
        '''PUT,dg%%'?%%%%%%%%%@%%%%%%%%:ounSs%%tb/%UT,dg%%'?%%%%%%%%%@%%%%%%%%ct/ Ss%%tb/%%%%%%%%%%è%%%%%%%+%%%%%%%%%"%%%%%%%%%%%%%%%DVtA''',
        #ORI

        #PSO
        "GET,¬abc",
        "GET,,ábc",
        "PUT,äatatb/product/,NweO",
        "PUT,datatb/product/,ÎweO",
        "POST,áccounts/login/,abcde",
        "POST,accounts/login/¬abcde",
        "GET,¬ab#",
        "GET,#ábc",
        "GET,%ábc",
        "GET,%abã",
        "PUT,äatatb%product/,NweO",
        "PUT,datatb%product/,ÎweO",
        "PUT,datatb;pct/,ÎweO",
        "PUT,datatb;pct,ìNweO",
        "GET,?áb#",
        "POST,,ccounts/login/,abcde",
        "PUT,D`4#pb;pct/,ÎweÏ",
        "PUT,dqtatf?pro/,wåO"
        "GET,¬abc",
        "GET,,ábc",
        "PUT,äatatb/product/,DVtaNweOCp",
        "PUT,datatb/product/,ÄVtaNweOCp",
        "POST,áccounts/login/,abcde",
        "POST,accounts/login/¬abcde",
        "GET,¬ab#",
        "GET,#ábc",
        "GET,%ábc",
        "GET,%abã",
        "PUT,äatatb%product/,DVtaCp",
        "PUT,datatb%product/,ÄVtaCp",
        "PUT,tb;product/,Ãp",
        "PUT,tb;product,ìCp",
        "GET,?áb#",
        "PUT,ãt%4DVta",
        "POST,,ccount,abc",
        "偕听䑡瑡瑢⽰  ⍴⼬",
        "PUT,ct/luntw?lngin/,ábcde",
        "GET,¬abc",
        "GET,,ábc",
        "POST,áccounts/login/,abc",
        "POST,accounts/login/¬abc",
        "PUT,áccounts/login/,abcd",
        "PUT,accounts/login/,ábcd",
        "GET,¬ab#",
        "GET,#ábc",
        "GET,%ábc",
        "GET,%abã",
        "GET,?ábc",
        "POST,,cc,abc",
        "POST,áccs%login/,abc",
        "POST,áccgin%4abc",
        "PUT,`ccoin/,ábcd",
        "啐ⱔ⍡潣湥獴爯杵獩Ⱟ "
        #PSO
    ]
    counter = 0

    for a in b:

        input = a.split(',')
        
        if(len(input) != 3):
            if len(input) == 1:
                input.append("")
                input.append("")
            if len(input) == 2:
                input.append("")

        counter += 1

        print("Bug {} seed:".format(counter) + a)
        main(input)
        print("============")

    os._exit(0)