class Caretaker:
    """
    Undo, Redo, and Backup, and clear are conatined here
    """
    def __init__(self, originator):
        # 
        self.originator = originator
        self._undo_stack = []
        self._redo_stack = []

    def backup(self):
        """
        saves the originator to a memento (state) and append this into the undo stack
        clear the redo stack to make sure we dont leave access
        """
        memento = self.originator.save()
        self._undo_stack.append(memento)
        self._redo_stack.clear() 

    def undo(self):
        """
        LIFO - pop the stack and restore the state
        """
        if len(self._undo_stack) > 1:
            memento = self._undo_stack.pop()
            self._redo_stack.append(memento)
            previous_state = self._undo_stack[-1]
            self.originator.restore(previous_state)

    def redo(self):
        """
        pop the redo stack and restore
        """
        if self._redo_stack:
            memento = self._redo_stack.pop()
            self._undo_stack.append(memento)
            self.originator.restore(memento)

    def clear(self):
        """
        clear both of the stacks
        """
        self._undo_stack.clear()
        self._redo_stack.clear()
