import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
client_socket.connect(server_address)
print('Connected to the server')

# Receive the game start message
start_message = client_socket.recv(1024).decode('utf-8')
print(start_message)

# Get the user's choice
user_choice = input("Enter your choice (rock/paper/scissors): ").lower()

# Send the user's choice to the server
client_socket.sendall(user_choice.encode('utf-8'))

# Receive the game result from the server
result = client_socket.recv(1024)
print(result.decode('utf-8'))

# Close the connection
client_socket.close()
