import socket

bufferSize = 1024; # maximum size of transmission to listen for

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 50000)
client_socket.connect(server_address)
print('Connected to the server')

# Receive the game start message
start_message = client_socket.recv(bufferSize).decode('utf-8')
print(start_message)

# Get the user's choice - only first character necessary
user_choice = input("Enter your choice - (r)ock/(p)aper/(s)cissors): ").lower()[0]

# Send the user's choice to the server
client_socket.sendall(user_choice.encode('utf-8'))

# Receive the game result from the server
result = client_socket.recv(bufferSize)
print(result.decode('utf-8'))

# Close the connection
client_socket.close()
