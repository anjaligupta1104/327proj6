"""
Meili and Anjali Gupta
CPSC 327 Pset
Saturday, 3:30 pm
"""

import sys
from SantoriniCLI import SantoriniCLI

"""
Take in the command line args, then use them to set up a manager object that will drive the core game loop.
"""

if __name__ == "__main__":
    SantoriniCLI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).run()