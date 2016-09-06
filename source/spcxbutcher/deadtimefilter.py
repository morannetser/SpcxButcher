class DeadtimeFilter:
    def __init__( self, deadtime ):
        self._deadtime = deadtime
        self._previous = None

    def __call__( self, current ):
        if self._previous is None:
            self._previous = current
            return True

        if current.timestamp - self._previous.timestamp > self._deadtime:
            self._previous = current
            return True

        return False
