import socket
from RPS import * # for Windows getch() keypress funcitonality

player1_choice = player2_choice = ''
player1pts = player2pts = 0

def playARound(player1_choice, player2_choice):
    global player1pts, player2pts
    # Display the choices
    print('\nPlayer 1 chose:', player1_choice) #rpsRank.get(player1_choice)[1])
    print('Player 2 chose:', player2_choice) #rpsRank.get(player2_choice)[1])

    # Determine the winner
    if player1_choice == player2_choice:
        result = "It's a tie!"
    elif player1_choice == 'q' or player2_choice == 'q':
        print('\n') # for the server
        result = "A player has disconnected - GAME OVER!"
    elif rpsRank.get(player1_choice)[0] == rpsRank.get(player2_choice)[0]%3 + 1: 
#        result = f"Player 1 chose {rpsRank.get(player1_choice)[1]} - Player 1 wins!"
        result = "Player 1 wins!"
        player1pts += 1
    else:
        result = "Player 2 wins!"
        player2pts += 1

    print(result) # for the server

    # Send the result to both players, combine using f-strings
    player1_socket.sendall((f'{result} {player1pts} v {player2pts}').encode('utf-8'))
    player2_socket.sendall((f'{result} {player2pts} v {player1pts}').encode('utf-8'))



# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 50000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(2)
print('Server is listening for connections...')

# Accept the first player's connection
player1_socket, player1_address = server_socket.accept()
print('Player 1 connected:', player1_address)

# Notify Player 1 to wait for Player 2
#sending this ends player1's game before they can see who won
#player1_socket.sendall("Waiting for another player to connect...".encode('utf-8'))
player1_socket.sendall("Welcome, Player 1. Waiting for player 2 to connect...".encode('utf-8'))

# Accept the second player's connection
player2_socket, player2_address = server_socket.accept()
print('Player 2 connected:', player2_address)

# Notify both players that the game is starting
player2_socket.sendall("Welcome, Player 2.".encode('utf-8'))
player1_socket.sendall("Both players connected. The game is starting!".encode('utf-8'))
player2_socket.sendall("Both players connected. The game is starting!".encode('utf-8'))
print("Both players connected. The game is starting!")

"""# START GAME - Prime the game loop by receiving choices from both players
player1_choice = player1_socket.recv(bufferSize).decode('utf-8')
player2_choice = player2_socket.recv(bufferSize).decode('utf-8')
"""
# GAME LOOP
while player1_choice != 'q' and player2_choice != 'q':
    # Receive choices from both players for the next round
    player1_choice = player1_socket.recv(bufferSize).decode('utf-8')
    player2_choice = player2_socket.recv(bufferSize).decode('utf-8')
    playARound(player1_choice, player2_choice)
    

print(f'Player 1: {player1pts}\nPlayer 2: {player2pts}')

# Close the connections
player1_socket.close()
player2_socket.close()
server_socket.close()
exit(0)

