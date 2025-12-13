from logging import getLogger
from git.exc import InvalidGitRepositoryError

from PySide6.QtCore import (
    QCoreApplication,
    QSettings,
    Qt,
    Slot,
)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from phystool.__version__ import __version__
from phystool.config import config
from phystool.qt.filter import FilterWidget
from phystool.qt.git import GitDialog
from phystool.qt.pdbfile import PdbFileListWidget
from phystool.qt.pdf import PdfWidget


logger = getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Phystool")
        QCoreApplication.setOrganizationName("phystool")
        QCoreApplication.setApplicationName("physnoob")

        filter_widget = FilterWidget()
        pdb_file_widget = PdbFileListWidget(filter_widget)
        pdf_widget = PdfWidget()
        self.setCentralWidget(pdf_widget)

        pdb_file_widget.sig_update_display.connect(pdf_widget.display)
        filter_widget.sig_filter_updated.connect(pdb_file_widget.update_list)
        filter_widget.filter_pdb_files()
        pdb_file_widget.setCurrentCell(0, 0)

        title_search_widget = QLineEdit()
        title_search_widget.setPlaceholderText("Rechercher dans le titre")
        title_search_widget.textChanged.connect(pdb_file_widget.search_in_title)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.addWidget(pdb_file_widget)
        list_layout.addWidget(title_search_widget)

        dock = QDockWidget("Filtres")
        dock.setObjectName("dock/filtres")
        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        dock.setWidget(filter_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

        dock = QDockWidget("Liste")
        dock.setObjectName("dock/liste")
        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        dock.setWidget(list_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

        dock = QDockWidget("Compilation")
        dock.setObjectName("dock/compilation")
        dock.setWidget(pdb_file_widget.compilation_error_widget)
        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
            | QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        dock.hide()
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

        # TODO: defining menu in dedicated class
        menu = self.menuBar()
        main_menu = menu.addMenu("&Phystool")
        self._add_action_menu("&About", None, self._about, main_menu)

        menu_database = main_menu.addMenu("Changer de DB")
        for db_name in config.get_db_list():
            self._add_action_menu(
                db_name,
                None,
                pdb_file_widget.load_db,
                menu_database,
            )

        main_menu.addSeparator()
        self._add_action_menu(
            "&Quitter",
            QKeySequence.StandardKey.Quit,
            self._quit,
            main_menu,
        )

        file_menu = menu.addMenu("&File")
        self._add_action_menu(
            "&Importer",
            QKeySequence("Ctrl+I"),
            pdb_file_widget.import_pdb_file,
            file_menu,
        )
        self._add_action_menu(
            "&Nouveau",
            QKeySequence.StandardKey.New,
            pdb_file_widget.new_pdb_file,
            file_menu,
        )
        self._add_action_menu(
            "&Suprimer",
            QKeySequence.StandardKey.Delete,
            pdb_file_widget.delete_pdb_file,
            file_menu,
        )
        file_menu.addSeparator()
        self._add_action_menu(
            "&Ouvrir",
            QKeySequence.StandardKey.Open,
            pdb_file_widget.open_tex_file,
            file_menu,
        )
        self._add_action_menu(
            "&Editer les tags",
            QKeySequence("Ctrl+E"),
            pdb_file_widget.edit_pdbfile_tags,
            file_menu,
        )
        self._add_action_menu(
            "&Copier",
            QKeySequence.StandardKey.Copy,
            pdb_file_widget.copy_to_clipboard,
            file_menu,
        )

        meta_menu = menu.addMenu("&Metadata")
        self._add_action_menu(
            "Créer un nouveau &tag",
            None,
            filter_widget.create_new_tag,
            meta_menu,
        )
        self._add_action_menu(
            "Consolider la &DB",
            None,
            pdb_file_widget.consolidate,
            meta_menu,
        )
        self._add_action_menu(
            "&Stage and commit",
            QKeySequence("Ctrl+G"),
            self._git_stage_and_commit,
            meta_menu,
        )

        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/geometry"))
        self.restoreState(settings.value("MainWindow/windowState"))

    def _add_action_menu(
        self,
        name: str,
        shortcut: QKeySequence | QKeySequence.StandardKey | None,
        method,
        menu,
    ) -> None:
        action = QAction(name, self)
        if shortcut:
            action.setShortcuts(shortcut)
        action.triggered.connect(method)
        menu.addAction(action)

    @Slot()
    def _quit(self) -> None:
        settings = QSettings()
        settings.setValue("MainWindow/geometry", self.saveGeometry())
        settings.setValue("MainWindow/windowState", self.saveState())
        QApplication.quit()

    @Slot()
    def _about(self) -> None:
        msg = QMessageBox(self)
        status, links = __version__.get_status()
        about = "<h4>Version actuelle: {}</h4><h4>{}</h4><ul>{}</ul>".format(
            __version__,
            status,
            "".join(
                [
                    f"<li><a href='{value}'>{key}</a></li>"
                    for key, value in links.items()
                ]
            ),
        )
        msg.setText(about)
        msg.exec()

    @Slot()
    def _git_stage_and_commit(self) -> None:
        try:
            dialog = GitDialog(self)
            dialog.exec()
        except InvalidGitRepositoryError:
            pass
            # TODO: sent message


class PhysQt(QApplication):
    def __init__(self):
        super().__init__([])
        self.window = MainWindow()
        self.window.show()
