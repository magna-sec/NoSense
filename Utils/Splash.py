from termcolor import colored, cprint
from random import choice as rchoice


COLOURS = ["blue","cyan","dark_grey","green","light_blue","light_cyan","light_green","light_grey","light_magenta","light_red","light_yellow","magenta","red","white","yellow"]

DIVIDE = """
  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \\
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'"""

NoSense = [
  "                                                "
 ,"     __      __                       ____  "
 ,"  /\ \ \___ / _\ ___ _ __  ___  ___  |___ \ "
 ," /  \/ / _ \\\ \ / _ \ '_ \/ __|/ _ \   __) |"
 ,"/ /\  / (_) |\ \  __/ | | \__ \  __/  / __/"
 ,"\_\ \/ \___/\__/\___|_| |_|___/\___| |_____|"
 ,"Even Less Sense"]


def display_splash() -> None:
    """
    """
    # Clears the screen
    print("\033c", end="")
    
    # Random colours go brr
    borderColour = rchoice(COLOURS)
    print(colored(DIVIDE, borderColour)) 
    # Making each line a different colour
    for i in NoSense:
        print(colored(i, rchoice(COLOURS)))
    print(colored(DIVIDE, borderColour))