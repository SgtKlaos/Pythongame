class _Getch:
    """Gets a single character from standard input in Windows without needing to press enter.  
    Does not echo to the screen."""
    def __init__(self):
        import msvcrt
        self.msvcrt = msvcrt

    def __call__(self):
#        import msvcrt
        return self.msvcrt.getch()

getch = _Getch()
char = getch().decode('utf-8')

print(f"Character read: {char}")