from socket import *

server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
with open("data/tiny_shakespear.txt", "r") as f:
    dataset = f.read()
print("Server is ready to recieve")

while True:
    BUFFER_SIZE = 2 * 1024 * 1024 # 2 MB    
    client_request, client_address = server_socket.recvfrom(BUFFER_SIZE)
    client_request = client_request.decode()
    if client_request == "tiny":
        server_response = dataset
    else:
        server_response = "Dataset is not yet available, Only tiny is available at the moment"
    
    server_socket.sendto(
        server_response.encode(),
        client_address
    )
    print(f"Successfully sent {server_response} to {client_address}")