from qtpy.QtGui import QPainter, QPaintEvent
from qtpy.QtWidgets import QWidget


class EyeWidget(QWidget):
    """ Widget with a Eye drawn on top of it to represent the idea of
    viewing an object
    """
    def __init__(self, *args, **kwargs) -> None:
        """ Constructor
        """
        super().__init__(*args, **kwargs)
        self._cross_eye = False

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        """ Paint the button

        Args:
            a0 (QPaintEvent | None): Associated QPaintEvent
        """
        def round_to_even(val: float | int) -> int:
            return int(val / 2.) * 2

        super().paintEvent(a0)

        # Prepare coordinates
        frame_w = self.width()
        frame_h = self.height()
        center_x = int(frame_w / 2.)
        center_y = int(frame_h / 2.)
        pupil_size = round_to_even(frame_h * 0.3)
        border_height = round_to_even(frame_h * 0.4)
        border_width = round_to_even(frame_w * 0.4)
        border_width = min(border_width, border_height * 2)

        # Setup the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = painter.pen().color()
        painter.setBrush(color)
        pen = painter.pen()
        pen.setWidth(1)
        painter.setPen(pen)

        # Draw eye pupil
        painter.save()
        width = pupil_size
        height = pupil_size
        x = int(center_x - (width / 2))
        y = int(center_y - (height / 2))
        painter.drawEllipse(x, y, width, height)
        painter.restore()

        # Draw eye border
        painter.save()
        height = border_height
        width = border_width
        x = int(center_x - (width / 2))
        y = int(center_y - (height / 2))
        painter.drawArc(x, y, width, height, 0, 360*16)
        painter.restore()

        # Draw cross
        if self._cross_eye:
            painter.save()
            painter.drawLine(x, y, x + width, y + height)
            painter.drawLine(x, y + height, x + width, y)
            painter.restore()

    def setEnabled(self, a0: bool) -> None:
        """ Set the widget enabled value.

        If widget is disabled, will add a cross in the eye to emphasize that
        the widget is disabled

        Args:
            a0 (bool): enable value to set
        """
        super().setEnabled(a0)
        self._cross_eye = not a0
