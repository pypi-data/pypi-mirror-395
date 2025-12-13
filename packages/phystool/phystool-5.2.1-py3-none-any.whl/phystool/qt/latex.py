from logging import getLogger
from pathlib import Path
from collections.abc import Callable
from typing import cast

from PySide6.QtCore import Slot, QProcessEnvironment
from PySide6.QtWidgets import QDockWidget, QPlainTextEdit

from phystool.config import config
from phystool.helper import should_compile
from phystool.latex import PdfLatex, LatexLogParser, ErrorMessage, Latex3Message
from phystool.pdbfile import PDBFile
from phystool.qt.process import QManagedProcess


logger = getLogger(__name__)


class QPdfLatex(QManagedProcess):
    _ENVIRONMENT: QProcessEnvironment | None = None

    def __init__(
        self,
        pdb_file: PDBFile,
        post_compilation_hook: Callable[[PDBFile, str], None],
    ):
        super().__init__()
        self._pdb_file = pdb_file
        self._tmp_tex_file: Path
        self._status = self.Status.PENDING
        self._post_compilation_hook = post_compilation_hook

    def _get_env(self) -> QProcessEnvironment:
        if self.__class__._ENVIRONMENT is None:
            self.__class__._ENVIRONMENT = QProcessEnvironment.systemEnvironment()
            self.__class__._ENVIRONMENT.insert("TEXINPUTS", f":{config.db.PHYSTEX}:")
        return self.__class__._ENVIRONMENT

    def __str__(self) -> str:
        return f"{self.__class__.__name__} <{self._pdb_file.uuid}>"

    def get_unique_id(self) -> str:
        return str(self._pdb_file.uuid)

    def get_ready(self) -> None:
        self._status = self.Status.RUNNING
        if not should_compile(self._pdb_file.tex_file):
            self._status = self.Status.SUCCESS
            return

        logger.info(f"Compile {self._pdb_file!r}")
        self._tmp_tex_file = self._pdb_file.create_tmp_tex_file()
        pdflatex = PdfLatex(self._tmp_tex_file)
        cmd = pdflatex.compilation_command()
        self.setProgram(cmd[0])
        self.setArguments(cmd[1:])
        self.setProcessEnvironment(self._get_env())
        self.finished.connect(self._handle_exit)

    @Slot(int)
    def _handle_exit(self, exit_code: int) -> None:
        if exit_code:
            self._status = self.Status.ERROR
            llp = LatexLogParser(self._tmp_tex_file, [ErrorMessage, Latex3Message])
            llp.process()
            msg = llp.as_text()
            logger.warning(msg)
            self._post_compilation_hook(self._pdb_file, msg)
            return

        try:
            pdflatex = PdfLatex(self._tmp_tex_file)
            if not self._pdb_file.standalone:
                pdflatex.move_pdf(self._pdb_file.tex_file.with_suffix(".pdf"))
            pdflatex.clean([".out", ".log", ".aux"])
            self._status = self.Status.SUCCESS
            self._post_compilation_hook(self._pdb_file, "")
        except PdfLatex.MoveError as e:
            logger.warning(e)
            self._status = self.Status.ERROR
            self._post_compilation_hook(self._pdb_file, str(e))


class CompilationErrorWidget(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setReadOnly(True)
        self.setMaximumBlockCount(5)
        self.setMaximumHeight(100)

    def __call__(self, txt: str) -> None:
        if txt:
            self.setPlainText(txt)
            cast(QDockWidget, self.parent()).show()
        else:
            cast(QDockWidget, self.parent()).hide()
