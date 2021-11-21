#!/usr/bin/python3

import os
import sys
import getopt
import datetime
from dateutil import parser
from requests_pkcs12 import get, post
from virtualfile import VirtualFile

import config

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

debug = 1
keyfile = ""
noncefile = ""

# Parse command line arguments
def print_usage(msg):
    print(msg + " Format: client.py [-du] [-e] [keyfile] [noncefile]")

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
else:
    if len(args) != 2:
        print_usage("Key and nonce file needed")
        exit(1)
    else:
        keyfile = args[0]
        noncefile = args[1]

if debug: 
    print("Download: " + str(download) + "\nEncrypt: " + str(encrypt))
    print("Loading client certificate from : " + config.client_cert)
    print("Loading server certificate from : " + config.server_cert)
    if encrypt:
        print("Key file path : " + keyfile)
        print("Nonce file path : " + noncefile)

filename = config.filename
file = VirtualFile(filename, encrypt, keyfile, noncefile)

# First GET the file to check if it has been modified elsewhere
r = get(config.host_addr + ":" + str(config.host_port) + config.host_endpoint, pkcs12_filename=config.client_cert, pkcs12_password="", verify=config.server_cert)

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

        if (not download and last_mod_remote > last_mod_local) or (download and last_mod_local > last_mod_remote):
            if not download and last_mod_remote > last_mod_local:
                result = yesno("The remote file is newer than the local one. Do you want to overwrite it?")
            if download and last_mod_local > last_mod_remote:
                result = yesno("The local file is newer than the remote one. Do you want to overwrite it?")
            if result == 'n':
                filename += "_remote"
                print("A new file will be created here with remote content : " + filename)
                print("Solve the conflict and update the new version")
                file.vappend(r.content)
                exit(0)

            if result != 'y':
                print("Invalid answer")
                exit(1)
    else:
        # If uploading and the file does not exist, exit
        if not download:
            print("The file at " + filename + " does not exist")
            exit(1)

if download:
    r = get(config.host_addr + ":" + str(config.host_port) + config.host_endpoint, pkcs12_filename=config.client_cert, pkcs12_password="", verify=config.server_cert)

    if r.status_code == 200:
        print("Received file from server. Saving to " + filename)
        file.vwrite(r.content)
else:
    # Upload the file
    newdata = file.vread()
    r = post(config.host_addr + ":" + str(config.host_port) + config.host_endpoint, pkcs12_filename=config.client_cert, pkcs12_password="", verify=config.server_cert, headers={'Content-Type': 'application/octet-stream'}, data=newdata)
        
