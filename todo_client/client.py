#!/usr/bin/python3

import os
from requests_pkcs12 import get
from dotenv import load_dotenv

load_dotenv('../.env')

debug = 1

host_addr = 'https://localhost'
host_port = 9999
host_endpoint = '/todos'
client_cert = '../' + os.environ.get('CLIENT_CERT')
server_cert = '../' + os.environ.get('SERVER_CERT')
filename = "todo.txt"

if debug:
    print("Loading client certificate from : " + client_cert)
    print("Loading server certificate from : " + server_cert)
r = get(host_addr + ":" + str(host_port) + host_endpoint, pkcs12_filename=client_cert, pkcs12_password="", verify=server_cert)

if r.status_code == 200:
    print("Got response 200 from server. Saving whatever response content to file")
    try:
        with open(filename, "wb") as bf:
            bf.write(r.content)
            bf.close()
    except:
        print("Exception while writing to file");

