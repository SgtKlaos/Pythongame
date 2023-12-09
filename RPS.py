# Rock, Paper, Scissors module

# Global variable declaration
result = ''
bufferSize = 1024; # maximum size of transmission to listen for
rpsRank = {
    'r': (1,"rock"),
    'p': (2,"paper"),
    's': (3,"scissors"),
}

class _Getch:
    """Gets a single character from standard input in Windows without needing to press enter.  
    Does not echo to the screen."""
    def __init__(self):
        import msvcrt
        self.msvcrt = msvcrt

    def __call__(self):
#        import msvcrt
        return self.msvcrt.getch()

getch = _Getch() # prep the function call
#char = getch().decode('utf-8')
#print(f"Character read: {char}")
