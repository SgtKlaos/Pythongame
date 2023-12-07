import socket
import pygame # for various game functionality
from RPS import * # for Windows getch() keypress funcitonality

window_size = 500
pygame.init()
window = pygame.display.set_mode((window_size * 1.75, window_size))
font = pygame.font.SysFont('Arial', 20)

user_choice = ''

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 50000)
client_socket.connect(server_address)
print('Connected to the server')

# Receive welcome message
start_message1 = client_socket.recv(bufferSize).decode('utf-8')
print(start_message1)

# Receive the game start message
start_message2 = client_socket.recv(bufferSize).decode('utf-8')
print(start_message2)

while user_choice != 'q' and result[0:len('A player has disconnected - GAME OVER!')] != 'A player has disconnected - GAME OVER!':
    # Get the user's choice - only first character necessary
    print("\nEnter your choice - (r)ock/(p)aper/(s)cissors/(q)uit") #user_choice = input("Enter your choice - (r)ock/(p)aper/(s)cissors): ").lower()[0]
    user_choice = getch().decode('utf-8')
    print(rpsRank.get(user_choice)[1])

    # Send the user's choice to the server
    client_socket.sendall(user_choice.encode('utf-8'))

    # Receive the game result from the server
    result = client_socket.recv(bufferSize).decode('utf-8')
    print(result)

# Close the connection
client_socket.close()
pygame.quit()