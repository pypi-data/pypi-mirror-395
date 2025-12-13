from collections import deque
from enum import Enum
from logging import getLogger

from PySide6.QtCore import QProcess, Slot

from phystool.config import config

logger = getLogger(__name__)


class QManagedProcess(QProcess):
    class Status(Enum):
        PENDING = 0
        RUNNING = 1
        SUCCESS = 2
        ERROR = 3

    def __init__(self):
        super().__init__()
        self._status = self.Status.PENDING

    def get_unique_id(self) -> str:
        raise NotImplementedError

    def get_ready(self) -> None:
        """
        This method is called right before the connection to ProcessManager._run_next is
        made. This hopefully ensures that ProcessManager._run_next is called after
        everything else.
        """
        raise NotImplementedError

    def state(self) -> QProcess.ProcessState:
        if self._status == self.Status.PENDING:
            return QProcess.ProcessState.Running
        return super().state()

    def is_running(self) -> bool:
        return self._status == self.Status.RUNNING

    def __del__(self):
        logger.debug(f"Cleaning process {self}")


class ProcessManager:
    def __init__(self) -> None:
        self._pending: deque[QManagedProcess] = deque()
        self._running: list[QManagedProcess] = []
        self._all_unique_ids: set[str] = set()

    def add(self, process: QManagedProcess) -> None:
        # To prevent duplicate processes (compiling the same file twice in a
        # row), the set self._all_unique_ids contains the pending and running
        # the maganged processes unique id..
        if process.get_unique_id() in self._all_unique_ids:
            return

        self._all_unique_ids.add(process.get_unique_id())
        logger.debug(f"Adding new process {process}")
        self._pending.append(process)
        self._run_next(0)

    @Slot(int)
    def _run_next(self, _: int = 0) -> None:
        tmp = []
        for process in self._running:
            if process.is_running():
                tmp.append(process)
            else:
                self._all_unique_ids.remove(process.get_unique_id())

        self._running = tmp
        if len(self._running) > 1:
            return
        try:
            process = self._pending.popleft()
            logger.debug(f"Starting process {process}")
            process.get_ready()
            process.finished.connect(self._run_next)
            process.start()
            self._running.append(process)
        except IndexError:
            logger.debug("No pending process")
            pass


class OpenFileProcess(QProcess):
    PROGRAM = config.EDITOR_CMD[0]
    ARGUMENTS = config.EDITOR_CMD[1:]

    def __init__(self, filenames: list[str]):
        super().__init__()
        self._filenames = filenames
        self.setProgram(self.PROGRAM)
        self.setArguments(self.ARGUMENTS + filenames)  # beware of list copy
        self.errorOccurred.connect(self._failed)
        self.startDetached()

    @Slot(QProcess.ProcessError)
    def _failed(self, error: QProcess.ProcessError) -> None:
        if error == QProcess.ProcessError.FailedToStart:
            warn = f"Error when calling '{self.PROGRAM}' "
            if self.ARGUMENTS:
                warn += f"with '{self.ARGUMENTS}' "
            warn += f"to edit the files {', '.join(self._filenames)}"
            logger.warning(warn)
        else:
            logger.error(f"unkown error {error}")
