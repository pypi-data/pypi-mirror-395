import sys
import os
sys.path.append(os.path.dirname(__file__))
try:
    from wheel_of_fortune.game import *
    from wheel_of_fortune.decorators import *
    from wheel_of_fortune.file_handler import *
except Exception:
    from game import *
    from decorators import *
    from file_handler import *
except:
    print('idk what could possibly have gone wrong')