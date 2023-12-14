import socket
import pygame # ensure 'pip install pygame' for various game functionality
import keyboard # ensure 'pip install keyboard'
from RPS import * # for Windows getch() keypress funcitonality

pygame.init()
server_address = ('localhost', 50000)
font = pygame.font.SysFont('Arial', 30)
font.bold = True
user_choice = ''
score = 0
won = -1
opps_choice = 0
window_scale = .7
window_width = 1536 * window_scale
window_height = 1024 * window_scale
window = pygame.display.set_mode((window_width, window_height))
ctrscreenW = window_width/2 #center screen shortcuts
ctrscreenH = window_height/2 #center screen shortcuts
surfSCORE = pygame.font.SysFont('Arial', 30)
surfSCORE.bold = True
surfSCORE = font.render('SCORE: 00', True, (0, 0, 0))

# Render/print "SCORE"
def printScore(score):
    global surfSCORE
    scoreBoard = "SCORE: " + str(score)
    surfSCORE.fill((140,206,230))
    surfSCORE = font.render(scoreBoard, True, (0, 0, 0))
#    surfSCORE = pygame.transform.scale(surfSCORE, 
#        (surfSCORE.get_rect().width * window_scale * .7, surfSCORE.get_rect().height * window_scale * .7))
    screen.blit(surfSCORE, (ctrscreenW - (surfSCORE.get_rect().width/2), 10))
    pygame.display.update(ctrscreenW - (surfSCORE.get_rect().width/2), 10, surfSCORE.get_rect().width, surfSCORE.get_rect().height)

background_image = pygame.image.load("assets/background2.jpeg") # Load the background image

# Create the Pygame window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Rock / Paper / Scissors - Network Skirmish")
background_image = pygame.transform.scale(background_image, (window_width, window_height))
screen.blit(background_image, (0, 0))
printScore(score)
pygame.display.update()


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
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
imgscale = .5 * window_scale
imgsize = 768 * imgscale
rockimg = pygame.transform.scale(
    pygame.image.load("assets/rock2.png"), (imgsize, imgsize))
paperimg = pygame.transform.scale(
    pygame.image.load("assets/paper2.png"), (imgsize, imgsize))
scissorsimg = pygame.transform.scale(
    pygame.image.load("assets/scissors2.png"), (imgsize, imgsize))

weapon = [
    rockimg,
    paperimg,
    scissorsimg
]

# to allow the client to proceed through the game loop if no input
client_socket.setblocking(False)
client_socket.settimeout(0.1) 
print("\nEnter your choice - (r)ock/(p)aper/(s)cissors/(q)uit") #user_choice = input("Enter your choice - (r)ock/(p)aper/(s)cissors): ").lower()[0]

def quit(self):
    print('Quitting game...')
    client_socket.close() # Close the connection
    pygame.quit()

# GAME LOOP
while user_choice != 'q' and result[0:len('A player has disconnected - GAME OVER!')] != 'A player has disconnected - GAME OVER!':
    # Process user input (keypresses)    
    eventlist = pygame.event.get(eventtype=pygame.KEYDOWN) #get only keypresses
    for e in eventlist:
#        print(e.key)
        # Parse players valid key input
        if e.key == pygame.K_r or e.key == pygame.K_p or e.key == pygame.K_s:
            user_choice = e.unicode
#            print(rpsRank.get(user_choice)[1])
            # Notify server of player choice
            client_socket.sendall(user_choice.encode('utf-8'))
            # My weapon is pasted into the middle of the screen, and centered
            screen.blit(weapon[int(rpsRank.get(user_choice)[0])-1], 
                (ctrscreenW - (imgsize/2), ctrscreenH - (imgsize/2)))
            pygame.display.update()
        elif e.key == pygame.K_q: # Send the quit message to the server and quit the game
            client_socket.sendall('q'.encode('utf-8'))   
            quit(0)
        else:
            user_choice = ''

    won = -1 # reset

    try:
        # Receive the game result from the server
        result = client_socket.recv(bufferSize).decode('utf-8')
    except socket.timeout:
        pass # Timeout handling... ignore
    else:
        if result != '': print(f"'{result}'")

        # Determine and react to opponent's choice (an int 0-3)
        if "It's a tie!" in result:
            surfBEATS = font.render("TIES", True, (255, 255, 255))
            opps_choice = int(rpsRank.get(user_choice)[0])-1
            print("\nEnter your choice - (r)ock/(p)aper/(s)cissors/(q)uit") #user_choice = input("Enter your choice - (r)ock/(p)aper/(s)cissors): ").lower()[0]

        elif "Player 1 wins!" in result:
            if player == 1: 
                won = 1
                score += 1
                printScore(score)
            surfBEATS = font.render("BEATS", True, (255, 0, 0))
            # lookup what opponent's weapon must be
            opps_choice = (rpsRank.get(user_choice)[0] - 1 - player)%3 #e.g. returns integer 0-2
            print("\nEnter your choice - (r)ock/(p)aper/(s)cissors/(q)uit") #user_choice = input("Enter your choice - (r)ock/(p)aper/(s)cissors): ").lower()[0]

        elif "Player 2 wins!" in result: 
            if player == -1: 
                won = 1
                score += 1
                printScore(score)
            surfBEATS = font.render("BEATS", True, (255, 0, 0))
            # lookup what opponent's weapon must be
            opps_choice = (rpsRank.get(user_choice)[0] - 1 + player)%3
            print("\nEnter your choice - (r)ock/(p)aper/(s)cissors/(q)uit") #user_choice = input("Enter your choice - (r)ock/(p)aper/(s)cissors): ").lower()[0]

        # My opponent's weapon is pasted to the left if it beats mine, to the right if mine beats it
#        print(f"rpsRank.get(user_choice)[0] - 1 + player: {rpsRank.get(user_choice)[0] - 1 + player}")
#        print(f"user: {user_choice}")
#        print(f"opps: {opps_choice}")
        screen.blit(weapon[opps_choice], 
            (ctrscreenW - (imgsize/2) + (won * window_width/3), 
            ctrscreenH - (imgsize/2)))

        # Render/print "BEATS" between weapons
        distFromCenter = (imgsize/2) + (surfBEATS.get_rect().width/2) # + (window_scale/15)
        screen.blit(surfBEATS, (
            ctrscreenW + distFromCenter * won - (surfBEATS.get_rect().width/2), 
            ctrscreenH - (surfBEATS.get_rect().height/2)))

        # Update the screen with any new graphics
        pygame.display.update()
        screen.blit(background_image, (0, 0)) #redraw the background for the next round
        printScore(score)

print('Your opponent has disconnected - GAME OVER!')
quit(0)