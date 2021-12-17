"""
Meili and Anjali Gupta
CPSC 327 Pset 6
"""

import sys
from SantoriniCLI_noGUI import SantoriniCLI
from memento import Caretaker

"""
Take in the command line args, then use them to set up a manager object that will drive the core game loop.
"""

if __name__ == "__main__":
    santorini = SantoriniCLI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    caretaker = Caretaker(santorini)
    caretaker.backup() # save initial state of board
    santorini.run(caretaker)