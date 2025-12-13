from PySide6.QtCore import QObject, Signal, QThread

class Worker(QObject):
    finished = Signal(object)  # send back result or None

    def __init__(self, job_func, *args, **kwargs):
        super().__init__()
        self._job_func = job_func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            result = self._job_func(*self._args, **self._kwargs)
        except Exception as e:
            result = e
        self.finished.emit(result)


class ThreadRunner(QThread):
    """QThread wrapper that auto‑removes itself from a container on finish."""
    _active_threads = set()

    def __init__(self, job_func, done_callback=None, *args, **kwargs):
        super().__init__()
        self._worker = Worker(job_func, *args, **kwargs)
        self._worker.moveToThread(self)
        self._done_callback = done_callback

        self.started.connect(self._worker.run)
        self._worker.finished.connect(self._handle_done)

        self.__class__._active_threads.add(self)

    def _handle_done(self, result):
        if callable(self._done_callback):
            self._done_callback(result)
        self.__class__._active_threads.discard(self)
        self.quit()
        self.wait()


