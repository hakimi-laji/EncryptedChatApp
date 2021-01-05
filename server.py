# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
import random
import string
from thread import *

# socket stuffs - dont bother
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided  
#if len(sys.argv) != 3:  
#   print ("Correct usage: $ python <IP address> <port number>") 
#  exit()  
  
# takes the first argument from command prompt as IP address  
#IP_address = str(sys.argv[1])  
  
# takes second argument from command prompt as port number  
#Port = int(sys.argv[2])  

# bind socket with inputted ip and port
IP_address = '192.168.1.10'
Port = 8081
server.bind((IP_address, Port)) 



# listens to client - can be up to 100 connected clients
print ("Waiting for connections...")
server.listen(100) 

list_of_clients = [] 

def clientthread(conn, addr): 

	# sends a welcome message to the client
    conn.send("This chat session is encrypted. Have fun!")

    while True: 
        try:
            message = conn.recv(2048) 
            if message: 
                # prints the message and address it came from
                print ("<" + addr[0] + "> " + message) 

				# Calls broadcast function to send message to all 
                broadcast(message, conn) 

            else: 
                # remove broken connection
                remove(conn) 
        except: 
            continue

# Using the below function, we broadcast the message to all clients
def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients != connection: 
			try: 
				clients.send(message) 
			except: 
				clients.close() 

				# if the link is broken, we remove the client 
				remove(clients) 

# remove object from list
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 

while True: 

	# Accepts a connection request and stores two parameters, conn and addr
    conn, addr = server.accept()

	# Maintains a list of clients for ease of broadcasting 
    list_of_clients.append(conn)

	# prints the address of the user that just connected 
    print (addr[0] + " connected")

	# creates and individual thread for every user that connects 
    start_new_thread(clientthread,(conn,addr))

conn.close() 
server.close() 
