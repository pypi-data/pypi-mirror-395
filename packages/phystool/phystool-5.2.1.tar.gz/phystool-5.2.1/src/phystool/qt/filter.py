from logging import getLogger
from typing import cast

from PySide6.QtCore import QSettings, Qt, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from phystool.config import config
from phystool.pdbfile import PDBFile
from phystool.physql.metadata import create_new_tag, filter_pdb_files
from phystool.tags import Tags


logger = getLogger(__name__)


class PDBTypeCheckBox(QCheckBox):
    def __init__(self, pdb_type: str, parent: QWidget, checked: bool):
        super().__init__(pdb_type.capitalize(), parent)
        self.setChecked(checked)
        self.pdb_type = pdb_type


class TagCheckBox(QCheckBox):
    def __init__(self, category: str, tag_name: str, parent: QWidget):
        super().__init__(tag_name, parent)
        self.setTristate(True)
        self.tags = Tags({category: {tag_name}})


class FilterWidget(QWidget):
    sig_filter_updated = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.filtered_pdb_files: list[PDBFile] = []
        self._query = ""
        self._uuid_bit = ""
        self._excluded_tags: Tags
        self._selected_tags: Tags
        self._selected_types: set[str]

        self._filters_layout = QHBoxLayout()
        self._pdb_types_layout = QHBoxLayout()
        self._search_widget = QLineEdit()
        self._search_widget.setPlaceholderText("Rechercher dans les fichiers '*.tex'")
        self._search_widget.returnPressed.connect(self._filter_query)

        layout = QVBoxLayout(self)
        layout.addWidget(self._search_widget)
        layout.addLayout(self._pdb_types_layout)
        layout.addLayout(self._filters_layout)

        self.load_settings()
        self.update_filter_pdb_types()
        self.update_filter_tags()

    def update_filter_pdb_types(self) -> None:
        while child := self._pdb_types_layout.takeAt(0):
            if tmp := child.widget():
                tmp.deleteLater()

        for pdb_type in config.db.PDB_TYPES.keys():
            button = PDBTypeCheckBox(pdb_type, self, pdb_type in self._selected_types)
            button.toggled.connect(self._filter_pdb_type)
            self._pdb_types_layout.addWidget(button)

    @Slot()
    def update_filter_tags(self) -> None:
        while child := self._filters_layout.takeAt(0):
            while subchild := child.takeAt(0):
                if tmp := subchild.widget():
                    tmp.deleteLater()
            if tmp := child.widget():
                tmp.deleteLater()

        for category, tags in Tags.manager.tags:
            layout = QVBoxLayout()
            label = QLabel(category.capitalize())
            label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

            layout.addWidget(label)
            for tag_name in tags:
                button = TagCheckBox(category, tag_name, self)
                button.checkStateChanged.connect(self._filter_tags)
                if tag_name in self._selected_tags.data.get(category, []):
                    button.setCheckState(Qt.CheckState.Checked)
                elif tag_name in self._excluded_tags.data.get(category, []):
                    button.setCheckState(Qt.CheckState.PartiallyChecked)
                else:
                    button.setCheckState(Qt.CheckState.Unchecked)
                layout.addWidget(button)

            layout.addStretch()
            self._filters_layout.addLayout(layout)

    @Slot()
    def create_new_tag(self) -> None:
        dialog = QDialog()
        dialog.setWindowTitle("Create new tag for category")

        form = QFormLayout()
        category = QComboBox()
        category.addItems([cat.capitalize() for cat in Tags.manager.tags.data.keys()])
        category.setEditable(True)
        category.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        tag = QLineEdit()
        form.addRow("Category", category)
        form.addRow("Tag", tag)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)

        layout = QVBoxLayout(dialog)
        layout.addLayout(form)
        layout.addWidget(btn_box)

        if dialog.exec():
            create_new_tag(category.currentText().lower(), tag.text())
            self.update_filter_tags()

    def filter_pdb_files(self) -> None:
        self.filtered_pdb_files = filter_pdb_files(
            query=self._query,
            uuid_bit=self._uuid_bit,
            pdb_types=self._selected_types,
            selected_tags=self._selected_tags,
            excluded_tags=self._excluded_tags,
        )
        self.sig_filter_updated.emit()

    @Slot(Qt.CheckState)
    def _filter_tags(self, state: Qt.CheckState) -> None:
        button = cast(TagCheckBox, self.sender())
        if state == Qt.CheckState.PartiallyChecked:
            self._excluded_tags += button.tags
        elif state == Qt.CheckState.Checked:
            self._selected_tags += button.tags
            self._excluded_tags -= button.tags
        elif state == Qt.CheckState.Unchecked:
            self._selected_tags -= button.tags
        self.filter_pdb_files()

    @Slot()
    def _filter_pdb_type(self) -> None:
        button = cast(PDBTypeCheckBox, self.sender())
        if button.isChecked():
            self._selected_types.add(button.pdb_type)
        else:
            self._selected_types.remove(button.pdb_type)
        self.filter_pdb_files()

    @Slot()
    def _filter_query(self) -> None:
        self._query = self.sender().text()
        self.filter_pdb_files()

    def save_settings(self):
        settings = QSettings()
        settings.setValue(
            f"FilterWidget/excluded_tags_{config.db.NAME}",
            list(self._excluded_tags.as_ids()),
        )
        settings.setValue(
            f"FilterWidget/selected_tags_{config.db.NAME}",
            list(self._selected_tags.as_ids()),
        )
        settings.setValue(
            f"FilterWidget/selected_types_{config.db.NAME}",
            list(self._selected_types),
        )

    def load_settings(self) -> None:
        settings = QSettings()
        try:
            self._excluded_tags = Tags.manager.from_ids(
                cast(
                    set[int],
                    settings.value(f"FilterWidget/excluded_tags_{config.db.NAME}")
                    or set(),
                )
            )
            self._selected_tags = Tags.manager.from_ids(
                cast(
                    set[int],
                    settings.value(f"FilterWidget/selected_tags_{config.db.NAME}")
                    or set(),
                )
            )
            self._selected_types = set(
                cast(
                    set[str],
                    settings.value(f"FilterWidget/selected_types_{config.db.NAME}")
                    or set(),
                )
            )
        except Exception:
            logger.error(
                f"Reading stettings failed for {config.db.NAME}, using defaults"
            )
            self._excluded_tags = Tags({})
            self._selected_tags = Tags({})
            self._selected_types = set(config.db.PDB_TYPES.keys())

    def __del__(self):
        self.save_settings()
