from collections.abc import Callable

from PySide6.QtCore import (
    Signal,
    Slot,
    QObject,
    Qt,
    QRunnable,
    QThreadPool,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QProgressDialog,
    QWidget,
)


class WorkerSignals(QObject):
    finished = Signal(str)


class Worker(QRunnable):
    # https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/

    def __init__(self, fn: Callable[[], str]) -> None:
        super().__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    def run(self):
        try:
            msg = self.fn()
        except Exception as e:
            msg = str(e)
        self.signals.finished.emit(msg)


class QBusyDialog(QProgressDialog):
    def __init__(self, label: str, parent: QWidget):
        super().__init__(label, "", 0, 0, parent)
        self.setCancelButton(None)
        self.setWindowModality(Qt.WindowModality.WindowModal)

    @Slot(str)
    def _finished(self, msg: str) -> None:
        self.setCancelButtonText("Ok")
        self.setLabelText(msg)

    def run(self, task) -> None:
        self.show()
        worker = Worker(task)
        worker.signals.finished.connect(self._finished)
        QThreadPool.globalInstance().start(worker)


class MultipleSelectionWidget(QWidget):
    def __init__(self, left_labels: list[str], right_labels: list[str]):
        super().__init__()
        self.left = QListWidget()
        self.left.itemDoubleClicked.connect(self.move_to_right)
        self.left.setSortingEnabled(True)
        self.left.addItems(left_labels)

        self.right = QListWidget()
        self.right.itemDoubleClicked.connect(self.move_to_left)
        self.right.setSortingEnabled(True)
        self.right.addItems(right_labels)

        layout = QHBoxLayout(self)
        layout.addWidget(self.left)
        layout.addWidget(self.right)

    def _swap(self, a, b, item):
        row = a.row(item)
        a.takeItem(row)
        b.insertItem(0, item.text())

    @Slot()
    def move_to_right(self):
        self._swap(self.left, self.right, self.left.currentItem())

    @Slot()
    def move_to_left(self):
        self._swap(self.right, self.left, self.right.currentItem())

    def get_right_values(self) -> set[str]:
        return {self.right.item(i).text() for i in range(self.right.count())}
