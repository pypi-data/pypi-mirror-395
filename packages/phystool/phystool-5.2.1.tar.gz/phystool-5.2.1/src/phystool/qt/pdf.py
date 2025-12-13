from logging import getLogger

from PySide6.QtCore import QUrl, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView

from phystool.pdbfile import PDBFile


logger = getLogger(__name__)


class PdfWidget(QWebEngineView):
    def __init__(self) -> None:
        super().__init__()
        self.settings().setAttribute(self.settings().WebAttribute.PluginsEnabled, True)

    @Slot(PDBFile)
    def display(self, pdb_file: PDBFile) -> None:
        self.setUrl(QUrl(f"file:///{pdb_file.tex_file.with_suffix('.pdf')}"))
