from PyQt5 import QtCore, QtWidgets
from computation import Node


class DragButton(QtWidgets.QPushButton):

    redraw = QtCore.pyqtSignal(dict)

    def __init__(self, node,  node_id: int):
        super(DragButton, self).__init__(node)
        self.node_id = node_id

    def mousePressEvent(self, event):
        self._mousePressPos = None
        self._mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self._mousePressPos = event.globalPos()
            self._mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self._mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self._mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._mousePressPos is not None:
            moved = event.globalPos() - self._mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                new_data = {
                    "node_id": self.node_id,
                    "coords": self.geometry().getRect()
                }
                self.redraw.emit(new_data)
                return


        super(DragButton, self).mouseReleaseEvent(event)
