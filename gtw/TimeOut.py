import signal


class timeout:
    def __init__(self, seconds):
        self._seconds = seconds

    def __enter__(self):
        # Register and schedule the signal with the specified time
        signal.signal(signal.SIGALRM, timeout._raise_timeout)
        signal.alarm(self._seconds)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Unregister the signal so it won't be triggered if there is
        # no timeout
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

    @staticmethod
    def _raise_timeout(signum, frame):
        raise TimeoutError
