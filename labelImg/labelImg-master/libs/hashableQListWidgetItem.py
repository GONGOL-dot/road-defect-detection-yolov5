#!/usr/bin/env python
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    import sip

    sip.setapi("QVariant", 2)
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

# PyQt5: TypeError: unhashable type: 'QListWidgetItem'


class HashableQListWidgetItem(QListWidgetItem):
    def __init__(self, *args):
        super().__init__(*args)

    def __hash__(self):
        return hash(id(self))
