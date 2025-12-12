import sys
import os
sys.path.append(os.path.dirname(__file__))
try:
    from wheel_of_fortune.game import *
except:
    from game import *

if __name__ == '__main__':
    game()
    while 1:
        print("хотите начать игру? (д / н)")
        agree = input()
        if agree == 'д' or agree == 'Д':
            game()
        else:
            break