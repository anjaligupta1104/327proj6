"""
Meili and Anjali Gupta
CPSC 327 Pset
Monday, 12:42am

SantoriniCLI is the originator.
Created classes Memento and Caretaker.
"""

class Memento:
    def __init__(self, state):
        self._state = state # state is a tuple of (board, currPlayer, otherPlayer, turn)

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

    def __init__(self, originator) -> None:
        self._mementos = []
        self._originator = originator
        self._pointer = 0

    def backup(self) -> None:
        # saving originator state
        self._mementos.append(self._originator.save())

    def undo(self) -> None:
        # at turn 1 if self._pointer == 0
        if not self._pointer:
            return

        self._pointer -= 1 # decrement pointer by 1
        memento = self._mementos[self._pointer]

        # restoring state
        self._originator.restore(memento)

    def redo(self) -> None:
        # do nothing if already at latest turn
        if (self._pointer == (len(self._mementos) - 1)):
            return

        self._pointer += 1 # increment pointer by 1
        memento = self._mementos[self._pointer]

        # restoring state
        self._originator.restore(memento)

    def wipe(self) -> None:
        # wipe all turns to the right of pointer
        # new turn has been taken, invalidate any turns that could have been redone
        while((len(self._mementos) - 1) > self._pointer):
            self._mementos.pop()

    def incrementPointer(self):
        self._pointer += 1