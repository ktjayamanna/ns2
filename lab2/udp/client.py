from socket import *
from time import time

server_name = 'localhost'
server_port = 12000
client_socket = socket(
    AF_INET, # Specify IPV4 IP address family
    SOCK_DGRAM # Specifiy udp for this socket
)
message = input("Enter the data you want. \n Options: \n 1. tiny \n 2. large \n 3. huge \n")
start = time()
client_socket.sendto(
    message.encode(), # convert the text to a series of bytes (numbers)
    (server_name, server_port)
    )
end = time()
print(f"Time taken for UDP request: {end - start} seconds")
BUFFER_SIZE = 2 * 1024 * 1024 # 2 MB    
server_response, server_address = client_socket.recvfrom(BUFFER_SIZE)
print(server_response.decode())
client_socket.close()