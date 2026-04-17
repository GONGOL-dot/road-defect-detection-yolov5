try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


class ZoomWidget(QSpinBox):
    def __init__(self, value=100):
        super().__init__()
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setRange(1, 500)
        self.setSuffix(" %")
        self.setValue(value)
        self.setToolTip("Zoom Level")
        self.setStatusTip(self.toolTip())
        self.setAlignment(Qt.AlignCenter)

    def minimumSizeHint(self):
        height = super().minimumSizeHint().height()
        fm = QFontMetrics(self.font())
        width = fm.width(str(self.maximum()))
        return QSize(width, height)
