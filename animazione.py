import time
import colorama
from colorama import Fore, Back, Style
import os 

def anim(strlog):
    for x in range(len(strlog)):
        print(strlog[x], end='', flush=True)
        time.sleep(0.00)
        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')