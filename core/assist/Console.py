#Clears console without need to import any libraries
def clearConsole():
    print("\033[H\033[J", end="")