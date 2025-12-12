from quanti_fret.apps.gui.path import FretCaliConfigFileWidget

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout, QWidget


class StageFretCaliConfigFileWidget(QWidget):
    """ Widget containing only a layout and a FretCaliConfigFileWidget.

    This is to add it directly to the stages tabs as without the layout we
    loose the marging
    """

    def __init__(self, *args,  **kwargs) -> None:
        """ Constructor
        """
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        pathWidget = FretCaliConfigFileWidget(parent=self)
        layout.addWidget(pathWidget)
