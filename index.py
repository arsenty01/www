from PyQt5 import QtWidgets, QtCore, QtGui
from main_window import Ui_MainWindow
import sys


class Start(QtWidgets.QMainWindow):

    def __init__(self):
        super(Start, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # buttons connectors
        self.ui.count_logic.clicked.connect(self.start_logic)  # logical start count func
        self.ui.min_routes.clicked.connect(self.minimum_routes)  # minimum routes func
        self.ui.true_table.clicked.connect(self.show_table)  # show true table func
        self.ui.count_static.clicked.connect(self.start_static)  # static start count func
        self.ui.add_node.clicked.connect(self.add_node)  # fucking add node
        self.ui.clear.clicked.connect(self.clear)  # clear func

    def start_logic(self):
        """ """
        pass

    def minimum_routes(self):
        """ """
        pass

    def show_table(self):
        """ """
        pass

    def start_static(self):
        """ """
        pass

    def add_node(self):
        """ """
        pass

    def clear(self):
        """ """
        pass


app = QtWidgets.QApplication([])
application = Start()
application.show()

sys.exit(app.exec())
