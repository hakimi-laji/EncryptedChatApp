# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import string
import random
import base64


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#if len(sys.argv) != 3: 
#	print ("Correct usage: script, IP address, port number") 
#	exit() 
    
#IP_address = str(sys.argv[1]) 
#Port = int(sys.argv[2]) 

IP_address = '192.168.1.10'
Port = 8081
server.connect((IP_address, Port)) 




def encode(key, text):
    enc = []
    for i in range(len(text)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(text[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.b64encode("".join(enc))

def decode(message):
    # break down the encrypted string
    key = message[:100]
    enc = message[100:]
    
    dec = []
    enc = base64.b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)



while True: 
	# maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 

	# socket stuffs
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if len(message) < 99:
                print (message)
            else:
                decryptmsg = decode(message)
                print ("<Anonymous> " + decryptmsg)
                
        else: 
            # input message
            message = sys.stdin.readline() 
            
            # generate random key for every message
            key = str( ''.join(random.choice(string.ascii_letters) for i in range(100)))
            # encrypt message
            encryptmsg = key + encode(key, message)

            server.send(encryptmsg) 
            sys.stdout.write("<You> " + message)
            sys.stdout.flush() 
server.close() 
