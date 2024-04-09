from coapthon.client.helperclient import HelperClient
from coapthon import defines
from coapthon.resources.resource import Resource
import random
import string
import sys
import os
import afl

import getopt
import socket
import sys

from coapthon.utils import parse_uri

client = None


def usage():  # pragma: no cover
    print("Command:\tcoapclient.py -o -p [-P]")
    print("Options:")
    print("\t-o, --operation=\tGET|PUT|POST|DELETE|DISCOVER|OBSERVE")
    print("\t-p, --path=\t\t\tPath of the request")
    print("\t-P, --payload=\t\tPayload of the request")
    print("\t-f, --payload-file=\t\tFile with payload of the request")


def client_callback(response):
    print("Callback")


def client_callback_observe(response):  # pragma: no cover
    global client
    print("Callback_observe")
    check = True
    while check:
        chosen = eval(input("Stop observing? [y/N]: "))
        if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
            print("Unrecognized choose.")
            continue
        elif chosen == "y" or chosen == "Y":
            while True:
                rst = eval(input("Send RST message? [Y/n]: "))
                if rst != "" and not (rst == "n" or rst == "N" or rst == "y" or rst == "Y"):
                    print("Unrecognized choose.")
                    continue
                elif rst == "" or rst == "y" or rst == "Y":
                    client.cancel_observing(response, True)
                else:
                    client.cancel_observing(response, False)
                check = False
                break
        else:
            break

class CoAPFuzzer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = HelperClient(server=(self.host, self.port))
        # self.original_payload = "Hello, CoAP!"
        self.original_payload = "Random"
        

    def fuzz_and_send_requests_get(self):
        fuzzed_payload = self.original_payload
        print("Fuzzing payload:", fuzzed_payload)

        # Send fuzzed GET request with the fuzzed payload and path "/basic/"
        response = self.client.get("/basic", payload=fuzzed_payload)
        #self.client.post
        #self.client.close
        print(response.pretty_print())
        
    # def fuzz_and_send_requests_post(self):
    #     fuzzed_payload = self.original_payload
    #     print("Fuzzing payload:", fuzzed_payload)

    #     # Send fuzzed GET request with the fuzzed payload and path "/basic/"
    #     response = self.client.post("/basic", payload=fuzzed_payload)
        
    #     #self.client.post
    #     #self.client.close
    #     print(response.pretty_print())
        
    # def fuzz_and_send_requests_put(self):
    #     fuzzed_payload = self.original_payload
    #     print("Fuzzing payload:", fuzzed_payload)

    #     # Send fuzzed PUT request with the fuzzed payload and path "/basic/"
    #     response = self.client.put("/basic", payload=fuzzed_payload)
    #     #self.client.post
    #     #self.client.close
    #     print(response.pretty_print())

    def close_connection(self):
        self.client.stop()
        

def main(afl_input):
    host = "127.0.0.1"
    port = 5683
    
    op = afl_input[0]
    path = afl_input[1]
    payload = afl_input[2]

    fuzzer = CoAPFuzzer(host, port)
    
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:", ["help", "operation=", "path=", "payload=",
    #                                                            "payload_file="])
    # except getopt.GetoptError as err:
    #     # print help information and exit:
    #     print(str(err))  # will print something like "option -a not recognized"
    #     usage()
    #     sys.exit(2)
    # for o, a in opts:
    #     if o in ("-o", "--operation"):
    #         op = a
    #     elif o in ("-p", "--path"):
    #         path = a
    #     elif o in ("-P", "--payload"):
    #         payload = a
    #     elif o in ("-h", "--help"):
    #         usage()
    #         sys.exit()
    #     else:
    #         usage()
    #         sys.exit(2)

    # if op is None:
    #     print("Operation must be specified")
    #     usage()
    #     sys.exit(2)

    # if path is None:
    #     print("Path must be specified")
    #     usage()
    #     sys.exit(2)
    
    # if not path.startswith("coap://"):
    #     print("Path must be conform to coap://host[:port]/path")
    #     usage()
    #     sys.exit(2)

    #host, port, path = parse_uri(path)
    
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = fuzzer.client
    if op == "GET":
        if path is None:
            print("Path cannot be empty for a GET request")
            usage()
            sys.exit(2)
        response = client.get(path)
        print(response.pretty_print())
        client.stop()
    elif op == "OBSERVE":
        if path is None:
            print("Path cannot be empty for a GET request")
            usage()
            sys.exit(2)
        client.observe(path, client_callback_observe)
        
    elif op == "DELETE":
        if path is None:
            print("Path cannot be empty for a DELETE request")
            usage()
            sys.exit(2)
        response = client.delete(path)
        print(response.pretty_print())
        client.stop()
    elif op == "POST":
        if path is None:
            print("Path cannot be empty for a POST request")
            usage()
            sys.exit(2)
        if payload is None:
            print("Payload cannot be empty for a POST request")
            usage()
            sys.exit(2)
        response = client.post(path, payload)
        print(response.pretty_print())
        client.stop()
    elif op == "PUT":
        if path is None:
            print("Path cannot be empty for a PUT request")
            usage()
            sys.exit(2)
        if payload is None:
            print("Payload cannot be empty for a PUT request")
            usage()
            sys.exit(2)
        response = client.put(path, payload)
        print(response.pretty_print())
        client.stop()
    elif op == "DISCOVER":
        response = client.discover()
        print(response.pretty_print())
        client.stop()
    else:
        print("Operation not recognized")
        usage()
        sys.exit(2)
    
    # #while(1):
    # #    try:
    # fuzzer.fuzz_and_send_requests_get()
    # #    except:
    # fuzzer.close_connection()

if __name__ == "__main__":
    afl.init()
    
    a = sys.stdin.read()
    
    afl_input = a.split(',')
    
    if(len(afl_input) != 3):
        if len(afl_input) == 1:
            afl_input.append("")
            afl_input.append("")
        if len(afl_input) == 2:
            afl_input.append("")
    
    main(afl_input)
    os._exit(0)