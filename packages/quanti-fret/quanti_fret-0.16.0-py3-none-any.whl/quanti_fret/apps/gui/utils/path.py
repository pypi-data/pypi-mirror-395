import os

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget


class PathLabel(QWidget):
    """ Widget whose purpose is to display a Path.

    It is composed of two widgets aligned horizontaly:
        * A Title
        * A Non Editable line edit

    setPath automatically add the Path as the line edit widget tooltip
    """
    def __init__(self, title: str, *args, **kwargs):
        """ Constructor

        Args:
            title (str): title to display.
        """
        super().__init__(*args, **kwargs)

        # Layout
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Title
        titleLabel = QLabel(title, parent=self)
        layout.addWidget(titleLabel)

        # Path
        self._pathLineEdit = QLineEdit(parent=self)
        self._pathLineEdit.setReadOnly(True)
        layout.addWidget(self._pathLineEdit)

    def setPath(self, path: os.PathLike | str | None) -> None:
        """ Set a new Path

        Args:
            path (os.PathLike | str | None): Path to set
        """
        if path is None:
            path_str = ''
        else:
            path_str = str(path)
        self.setToolTip(path_str)
        self._pathLineEdit.setText(path_str)
