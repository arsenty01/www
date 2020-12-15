from PyQt5 import QtWidgets, QtCore, QtGui
from main_window import Ui_MainWindow
from computation import *
import sys


class Start(QtWidgets.QMainWindow):

    def __init__(self):
        super(Start, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.nodes_list = []

        # buttons connectors
        self.ui.count_logic.clicked.connect(self.start_logic)  # logical start count func
        self.ui.min_routes.clicked.connect(self.minimum_routes)  # minimum routes func
        self.ui.true_table.clicked.connect(self.show_table)  # show true table func
        self.ui.count_static.clicked.connect(self.start_static)  # static start count func
        self.ui.add_node.clicked.connect(self.add_node)  # fucking add node
        self.ui.clear.clicked.connect(self.clear)  # clear func

    def start_logic(self):
        """ """
        nodes = self.get_converted_nodes()
        technical_system = TechSystem(nodes)
        self.ui.lineEdit.setText(f'{technical_system.logic_method()}')

    def minimum_routes(self):
        """ """
        pass

    def show_table(self):
        """ """
        pass

    def start_static(self):
        """ """
        count = self.ui.tries_count_tf.text()
        if count:
            nodes = self.get_converted_nodes()
            technical_system = TechSystem(nodes)
            self.ui.lineEdit_3.setText(f'{technical_system.statistic_method(int(count))}')
        else:
            self.ui.lineEdit_3.setText('Введите кол-во испытаний')

    def add_node(self):
        """ """
        pass

    def clear(self):
        """ """
        pass

    def get_converted_nodes(self):
        """Конвертирует ui элементы в нужные элементы"""

        result_node_list = []
        for node in self.nodes_list:
            node_id = node.node_id
            p = node.p
            input_node = node.input_node
            output_node = node.output_node
            temp_node = Node(p, input_node, output_node, node_id)
            for linked in node.linked_nodes:
                temp_node.add_next_node(linked)
            result_node_list.append(temp_node)
        return result_node_list


app = QtWidgets.QApplication([])
application = Start()
application.show()

sys.exit(app.exec())
