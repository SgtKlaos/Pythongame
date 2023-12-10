import socket
import pygame # for various game functionality
from RPS import * # for Windows getch() keypress funcitonality

pygame.init()
#font = pygame.font.SysFont('Arial', 20)
user_choice = ''
opps_choice = 0
window_scale = .7
window_width = 1536 * window_scale
window_height = 1024 * window_scale
window = pygame.display.set_mode((window_width, window_height))

# Load the background image
background_image = pygame.image.load("assets/background2.jpeg")

# Create the Pygame window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Rock / Paper / Scissors - Network Skirmish")
background_image = pygame.transform.scale(background_image, (window_width, window_height))
screen.blit(background_image, (0, 0))
pygame.display.flip()


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 50000)
client_socket.connect(server_address)
print('Connected to the server')

# Receive welcome message
start_message1 = client_socket.recv(bufferSize).decode('utf-8')
print(start_message1)
# Check for player identity
if start_message1.find("Player 1") > 0: player = 1
if start_message1.find("Player 2") > 0: player = -1

# Receive the game start message
start_message2 = client_socket.recv(bufferSize).decode('utf-8')
print(start_message2)

# Load the weapon images into a dictionary
rockimg = pygame.transform.scale(pygame.image.load("assets/rock2.png"), (768 * .5 * window_scale, 768 * .5 * window_scale))
paperimg = pygame.image.load("assets/paper2.png")
scissorsimg = pygame.image.load("assets/scissors2.png")
#TODO: use actual size to scale images into window
imgsize = pygame.display.get_size(scissorsimg) 

weapon = [
    rockimg,
    paperimg,
    scissorsimg
]

while user_choice != 'q' and result[0:len('A player has disconnected - GAME OVER!')] != 'A player has disconnected - GAME OVER!':
    # Get the user's choice - only first character necessary
    print("\nEnter your choice - (r)ock/(p)aper/(s)cissors/(q)uit") #user_choice = input("Enter your choice - (r)ock/(p)aper/(s)cissors): ").lower()[0]
    user_choice = getch().decode('utf-8')
    print(rpsRank.get(user_choice)[1])

    # Send the user's choice to the server
    client_socket.sendall(user_choice.encode('utf-8'))

    # My weapon is pasted into the middle of the screen
    screen.blit(weapon[int(rpsRank.get(user_choice)[0])-1], (window_width/2 - 768/2, window_height/2 - 768/2))
    pygame.display.flip()
    
    # Receive the game result from the server
    result = client_socket.recv(bufferSize).decode('utf-8')
    print(result)

    # Determine opponent's choice (# 0-3)
    if result == "It's a tie!":
        opps_choice = int(rpsRank.get(user_choice)[0])-1
    elif result == "Player 1 wins!":
#TODO: FINISH FUNCTIONALITY
        opps_choice = (rpsRank.get(user_choice)[0] - 1 - player)%3 #e.g. returns integer 0-2
    elif result == "Player 2 wins!": # lookup what opponent's weapon must be
#TODO: FINISH FUNCTIONALITY
        opps_choice = (rpsRank.get(user_choice)[0] - 1 + player)%3

    # My opponent's weapon is pasted to the left if it beats mine, to the right if mine beats it
    screen.blit(weapon[opps_choice], (window_width/2 - 768/2 + player * 500, window_height/2 - 768/2))
#TODO: PRINT TO SCREEN BETWEEN THE IMAGES
    print("BEATS") #TO SCREEN

    # Update the screen with any new graphics
    pygame.display.flip()

# Close the connection
client_socket.close()
pygame.quit()