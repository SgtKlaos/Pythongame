import socket
from RPS import * # for Windows getch() keypress funcitonality

server_address = "localhost" #from cmd > ipconfig     #socket.gethostbyname(socket.gethostname()) #('localhost', 50000)
server_port = 50000


def playARound(p1_choice, p2_choice):
    global player1pts, player2pts
    
    if p1_choice == 'q' or p2_choice == 'q':
        print('\n') # for the server
        result = "A player has disconnected - GAME OVER!"
        return 0
    else:
        # Display the choices
        print('\nPlayer 1 chose:', rpsRank.get(p1_choice)[1])
        print('Player 2 chose:', rpsRank.get(p2_choice)[1])

        # Determine the winner
        if p1_choice == p2_choice:
            result = "It's a tie!"
        elif rpsRank.get(p1_choice)[0] == rpsRank.get(p2_choice)[0]%3 + 1: 
    #        result = f"Player 1 chose {rpsRank.get(p1_choice)[1]} - Player 1 wins!"
            result = "Player 1 wins!"
            player1pts += 1
        else:
            result = "Player 2 wins!"
            player2pts += 1

        print(result) # for the server

        # Send the result to both players, combine using f-strings
        player1_socket.sendall((f'{result} {player1pts} v {player2pts}').encode('utf-8'))
        player2_socket.sendall((f'{result} {player2pts} v {player1pts}').encode('utf-8'))

def get_player_choice(s):
    c = s.recv(bufferSize).decode('utf-8')
    if c != 'None' and (c in rpsRank or c == 'q'):
#        print(f"'{c}'")
        return c
    else:
        get_player_choice(s)

while True:
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((server_address, server_port))

    # Listen for incoming connections
    server_socket.listen(2)
    print(f'\nServer at {server_address} is listening for connections...')

    # Accept the first player's connection
    player1_socket, player1_ip = server_socket.accept()
    print('Player 1 connected:', player1_ip)

    # Notify Player 1 to wait for Player 2
    player1_socket.sendall("Welcome, Player 1. Waiting for player 2 to connect...".encode('utf-8'))

    # Accept the second player's connection
    player2_socket, player2_ip = server_socket.accept()
    print('Player 2 connected:', player2_ip)

    # Notify both players that the game is starting
    player2_socket.sendall("Welcome, Player 2.".encode('utf-8'))
    player1_socket.sendall("Both players connected. The game is starting!".encode('utf-8'))
    player2_socket.sendall("Both players connected. The game is starting!".encode('utf-8'))
    print("Both players connected. The game is starting!")

    player1pts = player2pts = 0
    p1_choice = p2_choice = ''

    # GAME LOOP
    while p1_choice != 'q' and p2_choice != 'q':
        # Receive valid choices from both players for the next round
        p1_choice = get_player_choice(player1_socket)
        p2_choice = get_player_choice(player2_socket)
        playARound(p1_choice, p2_choice)

    print(f'Final Score\nPlayer 1: {player1pts}\nPlayer 2: {player2pts}')

    # Close the connections... to reopen them freshly
    player1_socket.close()
    player2_socket.close()
    server_socket.close()

exit(0)