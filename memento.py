"""
Meili and Anjali Gupta
CPSC 327 Pset
Monday, 12:42am
"""

from SantoriniCLI import SantoriniCLI

"""
SantoriniCLI is the originator.
Created classes Memento and Caretaker.
"""

class Memento:
    def __init__(self, state):
        self._state = state # state is a tuple of (board, player1, player2, currPlayer, turn)

    def get_state(self):
        """
        The Originator uses this method when restoring its state.
        """
        return self._state

class Caretaker():
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """

    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._originator = originator

    def backup(self) -> None:
        # saving originator state
        self._mementos.append(self._originator.save())

    def undo(self) -> None:
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        # restoring state
        self._originator.restore(memento)
