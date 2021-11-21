#!/usr/bin/python3

import os
import sys
import getopt
import datetime
from dateutil import parser
from requests_pkcs12 import get, post
from dotenv import load_dotenv

load_dotenv('../.env')
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

# Define options and constants
debug = 1
host_addr = 'https://localhost'
host_port = 9999
host_endpoint = '/todos'
client_cert = '../' + os.environ.get('CLIENT_CERT')
server_cert = '../' + os.environ.get('SERVER_CERT')
filename = "todo.txt"

# Parse command line arguments
def print_usage(msg):
    print(msg + " Format: client.py [-du] [-e]")

def yesno(msg):
    inp = ""
    while not inp:
        print(msg + " y/n : ");
        inp = input()
        if (inp != "y" and inp != "n"):
            inp = ""
    return inp
    

argv = sys.argv[1:]
download = True
encrypt = True
try:
    opts, args = getopt.getopt(argv, 'due')
    opts = [x[0] for x in opts]
except:
    print_usage("Invalid option.")
    exit(1)

if '-u' in opts:
    if '-d' in opts:
        print_usage("Can only do one operation at a time")
        exit(1)
    download = False

if '-e' not in opts:
    encrypt = False

if debug: 
    print("Download: " + str(download) + "\nEncrypt: " + str(encrypt))
    print("Loading client certificate from : " + client_cert)
    print("Loading server certificate from : " + server_cert)

if download:
    r = get(host_addr + ":" + str(host_port) + host_endpoint, pkcs12_filename=client_cert, pkcs12_password="", verify=server_cert)

    if r.status_code == 200:
        print("Got response 200 from server. Saving whatever response content to file")
        try:
            with open(filename, "wb") as bf:
                bf.write(r.content)
                bf.close()
        except:
            print("Exception while writing to file");
else:
    # First GET the file to check if it has been modified elsewhere
    r = get(host_addr + ":" + str(host_port) + host_endpoint, pkcs12_filename=client_cert, pkcs12_password="", verify=server_cert)

    if (not r.headers['Last-Modified']):
        result = yesno("Could not check for last modified date. Continue?")
        if result != 'y':
            print("Aborting")
            exit(2)
    else:
        if (os.path.exists(filename)):
            last_mod_remote = parser.parse(r.headers['Last-Modified'])
            last_mod_local = datetime.datetime.fromtimestamp(os.path.getmtime(filename), LOCAL_TIMEZONE)
            if debug:
                print("Remote file timestamp: " + str(last_mod_remote))
                print("Local file timestamp: " + str(last_mod_local))

            if (last_mod_remote > last_mod_local):
                result = yesno("The remote file is newer than the local one. Do you want to overwrite it?")
                if result == 'n':
                    filename += "_remote"
                    print("A new file will be created here with remote content : " + filename)
                    print("Solve the conflict, update the local file and then redo an upload")
                    try:
                        with open(filename, "wb") as bf:
                            bf.write(r.content)
                            bf.close()
                    except:
                        print("Exception while writing to file");
                    exit(0)

                if result != 'y':
                    print("Invalid answer")
                    exit(1)
    
    # Upload the file
    with open(filename, "rb") as rf:
        r = post(host_addr + ":" + str(host_port) + host_endpoint, pkcs12_filename=client_cert, pkcs12_password="", verify=server_cert, headers={'Content-Type': 'application/octet-stream'}, data=rf.read())
        rf.close()
        
