from logging import getLogger
from pathlib import Path
from typing import cast
from rapidfuzz.process import extract
from rapidfuzz.fuzz import QRatio
from shutil import copyfile
from time import sleep
from uuid import uuid4

from PySide6.QtCore import (
    Qt,
    QObject,
    Slot,
    Signal,
    QFileSystemWatcher,
)
from PySide6.QtGui import (
    QAction,
    QGuiApplication,
    QColor,
    QColorConstants,
    QContextMenuEvent,
)
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHeaderView,
    QMenu,
    QMessageBox,
    QProgressDialog,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from sqlalchemy.sql.expression import select

from phystool.config import config
from phystool.helper import should_compile
from phystool.pdbfile import PDBFile
from phystool.physql import physql_db
from phystool.physql.models import PDBRecord, PDBType
from phystool.physql.metadata import create_sql_database, remove_pdb_files, update_tags
from phystool.qt.helper import MultipleSelectionWidget
from phystool.qt.latex import QPdfLatex, CompilationErrorWidget
from phystool.qt.process import ProcessManager, OpenFileProcess
from phystool.qt.filter import FilterWidget
from phystool.tags import Tags


logger = getLogger(__name__)


class _CategoryTagsWidget(MultipleSelectionWidget):
    def __init__(self, category_name: str, ltags: Tags, rtags: Tags):
        super().__init__(
            ltags.data.get(category_name, []),
            rtags.data.get(category_name, []),
        )
        self.category_name = category_name


class _TagSelectionWidget(QDialog):
    def __init__(self, current_tags: Tags):
        super().__init__()
        self.setWindowTitle("Édition")

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Save
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        available_tags = Tags.manager.tags - current_tags
        self._widgets = [
            _CategoryTagsWidget(category_name, available_tags, current_tags)
            for category_name in Tags.manager.tags.data.keys()
        ]

        layout = QVBoxLayout(self)
        for widget in self._widgets:
            layout.addWidget(widget)
        layout.addWidget(btn_box)

    def get_new_tags_ids(self) -> set[int]:
        return {
            Tags.manager.get_id(widget.category_name, tag_name)
            for widget in self._widgets
            for tag_name in widget.get_right_values()
        }


class _TagAction(QAction):
    def __init__(
        self,
        tag_id: int,
        tag_name: str,
        adding: bool,
        trigger,
        parent: QObject,
    ):
        super().__init__(tag_name, parent)
        self._tag_id = tag_id
        self._adding = adding
        self.triggered.connect(trigger)

    def get_data(self) -> tuple[int, bool]:
        return self._tag_id, self._adding


class PdbFileListWidget(QTableWidget):
    sig_update_display = Signal(PDBFile)
    sig_consolidate = Signal()

    def __init__(self, filter_widget: FilterWidget) -> None:
        super().__init__()
        self._process_manager = ProcessManager()
        self._filter_widget = filter_widget
        self._row_title_map: dict[int, str] = {}
        self._watched: PDBFile
        self._watcher = QFileSystemWatcher()
        self._watcher.fileChanged.connect(self._auto_compilation)
        self._clipboard = QGuiApplication.clipboard()

        labels = ["Type", "Titre", "Tags"]
        self.setColumnCount(len(labels))
        self.setHorizontalHeaderLabels(labels)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.itemDoubleClicked.connect(self.open_tex_file)
        self.currentItemChanged.connect(self._display_pdb_file)

        header = self.horizontalHeader()
        header.setDefaultSectionSize(40)
        header.setMinimumSectionSize(40)
        header.resizeSection(1, 250)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.compilation_error_widget = CompilationErrorWidget()

    @Slot()
    def load_db(self) -> None:
        previous_db = config.DB_NAME
        config.DB_NAME = self.sender().text()
        self._filter_widget.save_settings()
        status = config.setup_db()
        if status == config.Status.READY:
            try:
                self.consolidate()
                self._filter_widget.load_settings()
                self._filter_widget.update_filter_pdb_types()
                self._filter_widget.update_filter_tags()
                self._filter_widget.filter_pdb_files()
                return
            except ValueError as e:
                logger.exception(e)
        else:
            logger.error(f"Configuration failed with status {status.name}")
        logger.debug(f"Reverting to {config.db}")
        config.DB_NAME = previous_db
        config.setup_db()

    def contextMenuEvent(self, arg__1: QContextMenuEvent) -> None:
        context = QMenu(self)
        for adding, submenu in [
            (True, QMenu("Ajouter un tag", context)),
            (False, QMenu("Supprimer un tag", context)),
        ]:
            context.addMenu(submenu)
            for category_name, tags in Tags.manager.tags:
                category_menu = QMenu(category_name, context)
                submenu.addMenu(category_menu)
                for tag_name in tags:
                    category_menu.addAction(
                        _TagAction(
                            tag_id=Tags.manager.get_id(category_name, tag_name),
                            tag_name=tag_name,
                            adding=adding,
                            trigger=self._batch_edit_pdbfile_tags,
                            parent=category_menu,
                        )
                    )

        context.exec(arg__1.globalPos())

    @Slot()
    def update_list(self) -> None:
        self.clearContents()
        self.setRowCount(len(self._filter_widget.filtered_pdb_files))
        self._row_title_map = {}
        for row, pdb_file in enumerate(self._filter_widget.filtered_pdb_files):
            self.setItem(row, 0, QTableWidgetItem(pdb_file.pdb_type.upper()[:3]))
            self.setItem(row, 1, QTableWidgetItem(pdb_file.title))
            self.setItem(row, 2, QTableWidgetItem(str(pdb_file.tags)))
            self._row_title_map[row] = pdb_file.title.lower()

    @Slot()
    def _display_pdb_file(self) -> None:
        row = self.currentRow()
        if row < 0:
            return
        self._watched = self._filter_widget.filtered_pdb_files[row]
        self._watch_and_compile()
        self.sig_update_display.emit(self._watched)

    @Slot(str)
    def _auto_compilation(self, path: str) -> None:
        """
        The small delay is required because when a file is saved, the OS copies
        the file before replacing the previous version. This means that for a
        brief period of time, python can't find the file. That's also why it
        disappears from the watch list and should only be re-added when it's
        safe.
        """
        fname = Path(path)
        i = 0
        while not fname.exists() and i < 10:
            i += 1
            sleep(0.1)

        if i == 10:
            logger.error(f"Watching {fname} failed")
            return
        self._watch_and_compile()

    def _watch_and_compile(self) -> None:
        if files := self._watcher.files():
            self._watcher.removePaths(files)
        self._watcher.addPath(str(self._watched.tex_file))
        if should_compile(self._watched.tex_file):
            pdf_latex = QPdfLatex(self._watched, self._post_compilation_hook)
            self._process_manager.add(pdf_latex)

    def _post_compilation_hook(self, pdb_file: PDBFile, msg: str) -> None:
        if self._watched == pdb_file:
            self.sig_update_display.emit(self._watched)
            self.compilation_error_widget(msg)

    def _get_selected_rows(self) -> set[int]:
        return {item.row() for item in self.selectedItems()}

    def _get_selected_pdb_file_map(self) -> dict[int, PDBFile]:
        return {
            row: self._filter_widget.filtered_pdb_files[row]
            for row in self._get_selected_rows()
        }

    @Slot()
    def edit_pdbfile_tags(self) -> None:
        row = self.currentRow()
        if row < 0:
            return

        pdb_file = self._filter_widget.filtered_pdb_files[row]
        dialog = _TagSelectionWidget(pdb_file.tags)
        if dialog.exec():
            with physql_db() as session:
                update_tags(
                    pdb_file,
                    session,
                    to_remove_ids=pdb_file.tags.as_ids(),
                    to_add_ids=dialog.get_new_tags_ids(),
                )
                self.setItem(row, 2, QTableWidgetItem(str(pdb_file.tags)))

    @Slot()
    def _batch_edit_pdbfile_tags(self) -> None:
        pdb_file_map = self._get_selected_pdb_file_map()
        tag_id, adding = cast(_TagAction, self.sender()).get_data()
        with physql_db() as session:
            for row, pdb_file in pdb_file_map.items():
                if adding:
                    update_tags(
                        pdb_file, session, to_add_ids={tag_id}, to_remove_ids=set()
                    )
                else:
                    update_tags(
                        pdb_file, session, to_add_ids=set(), to_remove_ids={tag_id}
                    )

                self.setItem(row, 2, QTableWidgetItem(str(pdb_file.tags)))

    @Slot()
    def open_tex_file(self) -> None:
        if filenames := [
            str(pdb.tex_file) for pdb in self._get_selected_pdb_file_map().values()
        ]:
            OpenFileProcess(filenames)

    @Slot()
    def consolidate(self) -> None:
        logger.info("Consolidate data")
        dialog = QProgressDialog("Consolidate data", "Cancel", 0, 1, self)
        dialog.setAutoClose(False)
        dialog.setAutoReset(False)
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.setMinimumDuration(0)
        dialog.setValue(1)

        _message = ""
        _n = 0
        for i, n, message in create_sql_database():
            if dialog.wasCanceled():
                return
            if _n != n:
                _n = n
                dialog.setMaximum(n)
            if _message != message:
                _message = message
                dialog.setLabelText(message)
            dialog.setValue(i)

        self._filter_widget.filter_pdb_files()
        self._filter_widget.update_filter_tags()

    @Slot()
    def delete_pdb_file(self) -> None:
        if pdb_files := self._get_selected_pdb_file_map().values():
            title = "Supression de fichiers"
            msg = (
                "<ul><li>"
                + "</li><li>".join(
                    [
                        "<h4>{}</h4><ul><li>{}</li><li>{}</li><li>{}</li></ul>".format(
                            pdb_file.uuid,
                            pdb_file.title,
                            pdb_file.pdb_type[:3].upper(),
                            pdb_file.tags,
                        )
                        for pdb_file in pdb_files
                    ]
                )
                + "</li></ul>"
            )
            button = QMessageBox.question(self, title, msg)
            if button == QMessageBox.StandardButton.Yes:
                remove_pdb_files([pdb_file.uuid for pdb_file in pdb_files])
                self._filter_widget.filter_pdb_files()
                msg = "Les fichiers sélectionnés ont bien été supprimés"
            elif button == QMessageBox.StandardButton.No:
                msg = "Les fichiers sélectionnés n'ont pas été supprimés"
            else:
                raise ValueError(button)
            QMessageBox.information(self, title, msg)

    @Slot()
    def import_pdb_file(self) -> None:
        title = "Importation d'un nouveau fichier"
        exts = "Tex Files (*.tex)"
        fname, _ = QFileDialog.getOpenFileName(self, title, str(Path.home()), exts)
        if not fname:
            return

        tex_file = Path(fname)
        if not tex_file.is_file():
            QMessageBox.warning(self, title, "Le fichier est introuvable")
            return

        if (
            QMessageBox.question(self, title, f"Importer '{tex_file}'?")
            == QMessageBox.StandardButton.No
        ):
            QMessageBox.information(
                self,
                title,
                f"Importation annulée.",
                buttons=QMessageBox.StandardButton.Ok,
            )
            return

        new_fname = (config.db.DB_DIR / str(uuid4())).with_suffix(".tex")
        copyfile(tex_file, new_fname)
        try:
            pdb_file = PDBFile.from_file(new_fname)
        except ValueError:
            new_fname.unlink()
            QMessageBox.warning(self, title, "Le type de PDBFile est indéterminé.")
            return

        pdb_file.save()
        with physql_db() as session:
            session.add(
                PDBRecord(
                    uuid=pdb_file.uuid,
                    title=pdb_file.title,
                    pdb_type=session.execute(
                        select(PDBType).filter_by(name=pdb_file.pdb_type)
                    ).scalar_one(),
                )
            )
        self._filter_widget.filter_pdb_files()

    @Slot()
    def new_pdb_file(self) -> None:
        OpenFileProcess([config.new_pdb_filename()])

    @Slot(str)
    def search_in_title(self, text: str) -> None:
        min_score = 100.0
        max_score = 0.0
        best_rows = dict()
        if text:
            best_rows = {
                row: score
                for _, score, row in extract(
                    text.lower(),
                    self._row_title_map,
                    limit=10,
                    processor=None,
                    scorer=QRatio,
                )
            }
            for score in best_rows.values():
                if score < min_score:
                    min_score = score
                if score > max_score:
                    max_score = score

        if not text or (max_score - min_score < 1):
            for row in range(self.rowCount()):
                if item := self.item(row, 1):
                    item.setBackground(QColorConstants.White)
                    self.showRow(row)
            return

        for row in range(self.rowCount()):
            if score := best_rows.get(row, 0):
                if item := self.item(row, 1):
                    item.setBackground(
                        QColor.fromHsvF(
                            0.28, (score - min_score) / (max_score - min_score), 0.9
                        )
                    )
                    if self.isRowHidden(row):
                        self.showRow(row)
            else:
                if not self.isRowHidden(row):
                    if item := self.item(row, 1):
                        item.setBackground(QColorConstants.White)
                        self.hideRow(row)

    @Slot()
    def copy_to_clipboard(self) -> None:
        if uuids := [
            str(pdb_file.uuid)
            for pdb_file in self._get_selected_pdb_file_map().values()
        ]:
            self._clipboard.setText("\n".join(uuids))
