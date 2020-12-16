from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor, QPen

from computation.node import Node
from crutch import DragButton
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
        new_node_id = len(self.nodes_list)+1
        input = True
        output = False
        p = 0.0

        self.ui.new_node = DragButton(self.ui.nodes, new_node_id)
        self.ui.new_node.setGeometry(20, 20, 90, 40)
        self.ui.new_node.setObjectName(f'node{new_node_id}')
        self.ui.new_node.setText(f'Элемент{new_node_id}: 0.0')
        self.ui.new_node.show()
        self.ui.new_node.redraw.connect(self.redraw)

        x = self.ui.new_node.geometry().getRect()[0]
        y = self.ui.new_node.geometry().getRect()[1]
        node = Node(p, input, output, new_node_id, x, y)
        self.nodes_list.append(node)
        self.redraw()

    def temp(self, new_data: dict):
        """ """

        for node in self.nodes_list:
            if node.node_id == new_data.get('node_id'):
                node.set_coordinates(*new_data.get('coords')[:2])

        self.redraw()

    def redraw(self):
        """ """

        self.ui.liner.setPen(QPen(QtCore.Qt.green, 2, QtCore.Qt.DashLine))
        self.ui.liner.begin(self)

        for node in self.nodes_list:
            if node.input_node:
                self.ui.liner.drawLine(10, 310, 30, 500)
            if node.output_node:
                self.ui.liner.drawLine(*node.get_center(), 761, 310)

            for n_node in node.next_nodes:
                self.ui.liner.drawLine(*node.get_center(), *n_node.get_center())
        self.ui.liner.end()

    def create_node(self):
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
