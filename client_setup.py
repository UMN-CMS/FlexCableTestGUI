#!/usr/bin/python3

import sys

ip_address = sys.argv[1]

with open("./PythonFiles/utils/server_ip.txt","w") as openfile:
    openfile.write(ip_address)

print("Server IP Address has been set to:", ip_address) 
