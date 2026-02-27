try:
    from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QWidget
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    import sip

    sip.setapi("QVariant", 2)
    from PyQt4.QtGui import QComboBox, QHBoxLayout, QWidget


class ComboBox(QWidget):
    def __init__(self, parent=None, items=[]):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.items = items
        self.cb.addItems(self.items)

        self.cb.currentIndexChanged.connect(parent.combo_selection_changed)

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def update_items(self, items):
        self.items = items

        self.cb.clear()
        self.cb.addItems(self.items)
