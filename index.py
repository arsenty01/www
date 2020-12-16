from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor, QPen

from computation.node import Node
from crutch import DragButton
from main_window import Ui_MainWindow
from sub_window import Ui_Dialog
from computation import *
import sys


class Start(QtWidgets.QMainWindow):

    send_data = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(Start, self).__init__()
        self.id_counter = 1
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.nodes_list = []
        self.ui_buttons_list = []

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
        new_node_id = self.id_counter
        self.id_counter += 1
        input = True
        output = True
        p = 0.0

        self.ui.new_node = DragButton(self.ui.nodes, new_node_id)
        self.ui.new_node.setGeometry(20, 20, 90, 40)
        self.ui.new_node.setObjectName(f'node{new_node_id}')
        self.ui.new_node.setText(f'Элемент{new_node_id}: 0.0')
        self.ui.new_node.clicked.connect(lambda: self.call_modal(new_node_id))
        self.ui.new_node.show()
        self.ui.new_node.redraw.connect(self.temp)
        self.ui_buttons_list.append(self.ui.new_node)

        x = self.ui.new_node.geometry().getRect()[0]
        y = self.ui.new_node.geometry().getRect()[1]
        node = Node(p, input, output, new_node_id, x, y)
        self.nodes_list.append(node)
        self.update()

    def call_modal(self, node_id: int):
        """ """

        self.modal = Modal(dataset={
            "nodes_list": self.nodes_list,
            "node_id": node_id
        })
        self.modal.exec()

    def temp(self, new_data: dict):
        """ """

        for node in self.nodes_list:
            if node.node_id == new_data.get('node_id'):
                node.set_coordinates(*new_data.get('coords')[:2])

        self.update()

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.redraw(qp)
        qp.end()

    def redraw(self, qp):
        """ """

        qp.setPen(QPen(QtCore.Qt.black))

        for node in self.nodes_list:
            if node.input_node:
                qp.drawLine(10, 310, *node.get_center())
            if node.output_node:
                qp.drawLine(*node.get_center(), 761, 310)

            for n_node in node.next_nodes:
                qp.drawLine(*node.get_center(), *n_node.get_center())

    def create_node(self):
        """ """
        pass

    def delete_node(self, node_id):
        """ """

        self.nodes_list = list(filter(lambda x: x.node_id != node_id, self.nodes_list))
        for node in self.nodes_list:
            node.next_nodes = list(filter(lambda x: x.node_id != node_id, node.next_nodes))
        deleted_node = list(filter(lambda x: x.node_id == node_id, self.ui_buttons_list))[0]
        deleted_node.hide()
        self.ui_buttons_list = list(filter(lambda x: x.node_id != node_id, self.ui_buttons_list))
        self.update()

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


class Modal(QtWidgets.QDialog):

    modal_closed = QtCore.pyqtSignal(dict)

    def __init__(self, dataset: dict):
        super(Modal, self).__init__()
        self.something = ''
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.dataset = dataset
        self.fill_data(dataset)


    def fill_data(self, dataset: dict):
        """ """
        nodes_list = dataset.get('nodes_list')

        for node in nodes_list:
            if node.get('node_id') == node.get('node_id')
                our_node = node

        self.ui.p_le.setText(our_node.p)


app = QtWidgets.QApplication([])
application = Start()
application.show()

sys.exit(app.exec())
