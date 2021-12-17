"""
Meili and Anjali Gupta
CPSC 327 Pset 6
"""

import sys
from SantoriniGUI import SantoriniGUI
from SantoriniCLI import SantoriniCLI
from memento import Caretaker

if __name__ == "__main__":
    santorini = SantoriniCLI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    caretaker = Caretaker(santorini)
    caretaker.backup() # save initial state of board
    SantoriniGUI(caretaker)