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
        # self.client.post
        # self.client.close
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

    # host, port, path = parse_uri(path)

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
    # afl.init()

    # a = sys.stdin.read()
    b = [  # PSO
        "GET,ôest",
        "GET,tåst",
        "POST,ôest,123",
        "POST,test,±23",
        "POST,test/ñ23",
        "PUT,ôest,123",
        "POST,ôest/12?",
        "PUT,,tesô/?",
        "GET,ôest,123",
        "GET,uåst,123",
        "GET,test/ñ23",
        "GET,ôest/12?",
        "GET,tesô,123",
        "POST,test//²?",
        # original afl
        "GET,�est,123",
        "GET,t�st,123",
        "GET,td�t,123",
        "GET,�est,123",
        "GET,test/�23",
        "POST,�est,123",
        "POST,test,�23",
        "PUT,�est,123",
        "GET,�est/12?",
        "GET,test//�?",
        "POST,teFFFFFFFFFFFF*FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfFFFFFFFFFFFFFFFFFFFFFFFFFFF%FFFFFFFFFFFFFFFFFFFFFFFFFF123FFFFFFAFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF2FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF-FFFFFFFFFFFFFFF FFPOST,FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF   FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFJFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF4FFFFFFFFFFFFFFFFFFFFFFFFFFFFaFFFFFFF<FFFFFFFFFFFFFFF-FFFFFrFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF3FFFFFFFeFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFSFFFFFÿÿFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF?FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGGFFF FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF?FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF123FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)FFFFFFFFFFFFFFFFFFFFFFFFFF:FFFÿFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF   FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGFFFFFFdFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFPOST,FFFFFCFFFFFFFFFFFFFFFFFFFGGGGGGFGHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG1GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG+GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGSGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGEGGGGGGGGGGGGG€GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG €ÿÿGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGÿ    €GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  FFFFFFFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFÿ hFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFoFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFbFFFFFFFFFFFFFFFFFFFFFFFFPFF   FFFFFFFFFFFFFFFFFFFF2F €  ^FFFFFFFFFFFFFFFFFFFFFFFFFÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFPUT,FFFFFFFFFFFFFFFFFGFFFFFFFFFFFFFFFFFFFGET,FFFFFFF(FFFFFFFFFFFFFFFFFFFFFFFZFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFdFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF123FFFFFFFFFFFFFFFFFFFFFFF%FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFRFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFPUT,FFFFFFFFF   FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFPOST,FFFFFFFFFFFFFFFFFFKFFFFFF   €FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  FFFFFFFF:FÿÿÿFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF&FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGET,FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFNFIFFFFFFFFFFFFFFF9FFFFFFFFFFFFFFFFFFFFF@FFFFFFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFFFFF5FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGETFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF123FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF=FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFtest,2?",
        "POST,teFFFFFFFFFFFF*FFFFFFFFFFFFFFFhFFFFFFFFFFFF.FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF FFFFFFF FFFFFFFFFFGETFFFFFFFFFFFFFFFFFFFUFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFè  FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFKFFFFFFFFFFFFFFFFFFFGETFFFFFFFFFFFFFFFRFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF€ FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF   @FFFFFFFFFFFFFFFFF”””””””””””””””””””””””FFFFFFFFFFFFFFFBFFFFFFFFFFFFFFéFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGET,FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF    FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF4FFFFFFFFFFFFFFFFF>FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGETFFFFFFFFFFFFFFFFFFFF5FFFFFFFFaFFFFFFFFFFFFFFFFFFFFFFFFFFFFFrFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFtest,2?",
        "䝅听 翿獴ÿ         ＿",
        "GET,ôest,123",
        "GET,tåst,123",
        "GET,test/ñ23",
        "GET, €   ô                          ,",
        "POST,ôest,123",
        "POST,test,±23",
        "PUT,ôest,123",
        "GET,ôest?123",
        "GET,test?&²3",
        "PUT,,ÿ",
        "GET,tesPU3333333333333333333333333333333333333333333333333333333333333333333333333333333C333333333.3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333M3333333333333333333333333333333333333333ÿÿÿÿ33333333333333333333333333333331333333T,3",
        "GET,ôest",
        "GET,te³t",
        "POST,ôest,12",
        "POST,test,±2",
        "POST,test/ñ2",
        "PUT,ôest,123",
        "POST,ôest?12",
        "POST,test?&²",
        "POST, te”””””””””””””””””””””””•&,",
        "GET,teesttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttptttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt\ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt{tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttGET,ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttd   ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt ttttttttttttttttttt   ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttPUT,ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttyttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt?&,",
        # afl + bucketing
        "GET,ôest,123",
        "GET,test¬123",
        "GET,test/ñ23",
        "GET,ëëëëÝëëÉ(RGQT,3",
        "POST,ôest,123",
        "POST,test,±23",
        "PUT,ôest,123",
        "POST,® T*    ?ÿþâ ­Â",
        "GET,test//²?",
        "PUT,,tå",
        'GET,test//esèQQQQQQQQQLQ55555555555555555555555555555555555155555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555D55555555555555555555555555555555555555555555555555555555555555555555555555555555555555€ 5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555     555K5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555POST,5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555R55555555555555555X555555555555555555555555555555555555555555V5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555   55555555555555555555555555555555555   5555555555555555555555555555555555555555u5555555GET,555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555L55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555<55555555555555555555555E555555555555555555555555555555555555555555555555555555555R55555555>55555555X5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555F5555555   5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555"555555555555555555555555555555555555555555555555555555555555555555QQQQQQQQ5QQQQQt//2?',
        "偕听潯潯潯潯潯潯潯潯漁o潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯豯潯驯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯筯潯潯潯潯澈潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潇䕔ṯ潯潯潯潯澑潯潯潯潯潯潯潯潯潯潯潯潯潯潯ｿ潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯慯偯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯偏協Ɐ潮潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯葯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯ｯ潯潯潯潯潯潯潯潯潯潯潯澅潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潴潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯敳瑯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯坯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯罯潯潯潯漠潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潞潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯婯潯潯潯潯潯浯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潨潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯攀 潯潯潯潯潯潯潯潯潯潯⽯潯潯潯潯潯潯潯潯潯潯潯潯潯澐潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潧潯潯潯潯潯潯澆潯潯潯潯潯潑潯潯潯潯潯潯潯潯潯濿翿ｯ潯潥獴潯潯潯潯潯潯潯潯潯潯潯潯潯潯潎潯赯潯潯潯潯潯潯潯潯潯潯潯潯潯詯潯潯潯潯衯潯潯潯潯潯潯潯潯潯潯澑潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潲潯潯潯潯潯潯潯潯潯潯潯쯋쯋쯋쭯潯潯潯潯潯潯潯潯潯潯潯潯潯濨ͯ潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯濯潯潯潯潯澐潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯澐潫潯穯潯潯潯潯潯潯潯澄潯潯潯潯潯潯潯潯潯潯潯潯潯潯蕯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潣潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯翿潯潯潯潯潯潯潯潯楯潯潯潯潯潯潯潯潯潯潯潯潯潯䝅听潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯漯潯潯潯潯潯潯潯潯潯潯潯潯潯潯遯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯潯⽯潯潯潯潯潯潯潯潯潯潯浯潯潯潯潯潯杯"

       
        

    counter = 0
    
for a in b:
        afl_input = a.split(',')
        
if(len(afl_input) != 3):
             if len(afl_input) == 1:
                afl_input.append("")
                afl_input.append("")
            if len(afl_input) == 2:
                afl_input.append("")
        
counter += 1

        print("Bug {} seed:".format(counter) + a)
        main(afl_input)
        print("============")
    os._exit(0)





                   
