from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QPainter, QPaintEvent
from qtpy.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget
)


class LoadingProgressLayout(QHBoxLayout):
    """ Layout containing a LoadingAnimationWidget and a QLabel that can
    display a loading animation associated along side with a text indicating a
    progress.

    You can put this layout inside another widget or layout. By default the
    widget is hidden. You can call `start()` to show the widget and start the
    animation. And you can call `stop()` to hide the widget and stop the
    animation. Finally, you can call `setProgress()` to set the progress
    message.
    """
    def __init__(
        self, interval: int = 1000, parent: QWidget | None = None
    ) -> None:
        """ Constructor

        Args:
            interval (int): interval in ms between two frames
        """
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self._animation = LoadingAnimationWidget(parent=parent)
        self._label = QLabel(parent=parent)
        self.addWidget(self._animation)
        self.addWidget(self._label)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Compute animation size
        label_height_hint = self._label.sizeHint().height()
        label_height = self._label.height()
        height = int((label_height_hint + label_height) / 2)
        self._animation.setMinimumHeight(height)
        self._animation.setMinimumWidth(height)

        self._label.hide()

    def start(self) -> None:
        """ Shows the widget and starts the animation
        """
        self._animation.start()
        self._label.setText('')
        self._label.show()

    def stop(self) -> None:
        """ Hides the widget and stops the animation
        """
        self._animation.stop()
        self._label.hide()

    def setProgress(self, progress: str) -> None:
        """ Set The progress message to be displayed alongside the animation

        Args:
            progress (str): Message to display
        """
        self._label.setText(progress)


class LoadingAnimationWidget(QWidget):
    """ Widget that displays a loading animation

    By default the widget is hidden. You can call `start()` to show the widget
    and start the animation. And you can call `stop()` to hide the widget and
    stop the animation.
    """
    def __init__(
        self, interval: int = 50, parent: QWidget | None = None
    ) -> None:
        """ Constructor

        Args:
            interval (int): interval in ms between two frames
        """
        super().__init__(parent=parent)

        # Animation
        self._angle = 0
        self._interval = interval
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.updateAnimation)

        # GUI
        self.hide()

    def start(self) -> None:
        """ Shows the widget and starts the animation
        """
        self._timer.start(self._interval)
        self.show()

    def stop(self) -> None:
        """ Hides the widget and stops the animation
        """
        self._timer.stop()
        self.hide()

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        """ Paint the animation for a single frame

        Args:
            a0 (QPaintEvent | None): Associated QPaintEvent
        """
        # Compute Geometry
        frame_w = self.width()
        frame_h = self.height()
        square_size = min(frame_w, frame_h)
        circle_size = square_size / 6
        dist = int(square_size / 4)
        size = int(circle_size)

        # Setup the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(frame_w / 2, frame_h / 2)
        color = painter.pen().color()
        painter.setBrush(color)

        # Draw each circles
        for i in range(4):
            painter.save()
            angle = (self._angle - 40 * i) % 360
            painter.rotate(angle)
            painter.drawEllipse(*self._toRectCoordonates(dist, size))
            size = size - 1
            painter.restore()

    def _toRectCoordonates(
        self, dist: int, size: int
    ) -> tuple[int, int, int, int]:
        """Transform coordinates representing the distance to the center of
        the circle and its size to a rect coordinates

        Args:
            dist (int): distance of the center of the circle to the center of
                the frame.
            size (int): size of the circle

        Returns:
            tuple[int, int, int, int]: Rectangle frame in which to draw the
                circle.
        """
        x = int(dist - size / 2)
        y = 0
        w = size
        h = size
        return x, y, w, h

    def updateAnimation(self) -> None:
        """ Update the animation by moving the circles angle
        """
        self._angle = (self._angle + 10) % 360
        self.update()


class LoadingAnimationLayout(QVBoxLayout):
    """ Layout containing a LoadingAnimationWidget that can display a loading
    animation.

    This class is just a layout containing the widget. It exists to be prevent
    the user to be forced to create a loayout.

    You can put this layout inside another widget or layout. By default the
    widget is hidden. You can call `start()` to show the widget and start the
    animation. And you can call `stop()` to hide the widget and stop the
    animation.
    """
    def __init__(
        self, interval: int = 50, parent: QWidget | None = None
    ) -> None:
        """ Constructor

        Args:
            interval (int): interval in ms between two frames
        """
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self._widget = LoadingAnimationWidget(interval, parent=parent)
        self.addWidget(self._widget)

    def start(self) -> None:
        """ Shows the widget and starts the animation
        """
        self._widget.start()

    def stop(self) -> None:
        """ Hides the widget and stops the animation
        """
        self._widget.stop()
