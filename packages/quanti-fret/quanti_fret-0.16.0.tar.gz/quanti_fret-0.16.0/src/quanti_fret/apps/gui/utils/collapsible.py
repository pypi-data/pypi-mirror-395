from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLayout,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class CollapsibleBox(QGroupBox):
    """ Box that can be expended or collapse because Qt doesn't come with such
    widget...
    """

    def __init__(self, title: str, *args, **kwargs) -> None:
        """ Constructor

        Args:
            title (str): Title of the Box
        """
        super().__init__(*args, **kwargs)

        # Build GUI
        self._mainLayout = QVBoxLayout()
        self._mainLayout.setContentsMargins(0, 7, 0, 7)
        self._mainLayout.setSpacing(0)
        self.setLayout(self._mainLayout)
        self._buildTitle(title)
        self._buildContent()
        self.setContentVisible(False)

        # Connect Slots
        self._arrow.clicked.connect(
            lambda: self._swapContentVisibility(self._arrow)
        )
        self._title.clicked.connect(
            lambda: self._swapContentVisibility(self._title)
        )

    def setContentVisible(self, visible: bool) -> None:
        """ Set the visibility of the content

        Args:
            visible (bool): True to set the content visible
        """
        self._arrow.setChecked(visible)
        self._title.setChecked(visible)
        if visible:
            self._content.show()
            self._arrow.setArrowType(Qt.ArrowType.DownArrow)
            self.setStyleSheet("CollapsibleBox {}")
        else:
            self._content.hide()
            self._arrow.setArrowType(Qt.ArrowType.RightArrow)
            self.setStyleSheet("CollapsibleBox {border :0px;}")

    def addContentWidget(self, widget: QWidget) -> None:
        """ Add the given widget to the content

        Args:
            widget (QWidget): Widget to add
        """
        self._content_layout.addWidget(widget)

    def addContentLayout(self, layout: QLayout) -> None:
        """ Add the given layout to the content

        Args:
            layout (QLayout): layout to add
        """
        self._content_layout.addLayout(layout)

    def _buildTitle(self, title: str) -> None:
        """ Build the title / button of the widget

        Args:
            title (str): Title of the Box
        """
        # Title Layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._mainLayout.addLayout(layout)

        # Arrow button
        # (This could have been in the self._title but I didn't manage to
        # reduce the size of just the arrow so I'm making two QToolButton)
        self._arrow = QToolButton(parent=self)
        self._arrow.setArrowType(Qt.ArrowType.RightArrow)
        self._arrow.setCheckable(True)
        self._arrow.setChecked(False)
        self._arrow.setStyleSheet("QToolButton { border: none; }")
        layout.addWidget(self._arrow)

        # Title
        self._title = QToolButton(parent=self)
        self._title.setText(title)
        self._title.setCheckable(True)
        self._title.setChecked(False)
        self._title.setStyleSheet("QToolButton { border: none; }")
        layout.addWidget(self._title)

        # Adjust arrow size
        self._arrow.setMaximumHeight(int(self._title.height()/2.5))

    def _buildContent(self) -> None:
        """ Build the content of the widget
        """
        # Create content widget
        self._content = QWidget(parent=self)
        self._content.hide()
        self._mainLayout.addWidget(self._content)

        # Content layout
        self._content_layout = QVBoxLayout()
        self._content.setLayout(self._content_layout)

    def _swapContentVisibility(self, button: QToolButton) -> None:
        """ Swap visibility of the widget's content

        Args:
            button (QToolButton): Button that was clicked
        """
        visible = button.isChecked()
        self.setContentVisible(visible)
