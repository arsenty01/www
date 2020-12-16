from typing import Any

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
        self.ui.count_static.clicked.connect(self.start_static)  # static start count func
        self.ui.add_node.clicked.connect(self.add_node)  # fucking add node
        self.ui.clear.clicked.connect(self.clear)  # clear func

    def start_logic(self):
        """ """
        nodes = self.nodes_list
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
            nodes = self.nodes_list
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
        self.modal.modal_closed.connect(self.edit_node)
        self.modal.exec()

    def edit_node(self, node):
        """"""
        self.nodes_list = list(filter(lambda x: x.node_id != node.node_id, self.nodes_list))
        next_nodes = list(filter(lambda x: x.node_id in node.next_nodes, self.nodes_list))
        node.next_nodes = next_nodes
        self.nodes_list.append(node)
        temp_node = list(filter(lambda x: x.node_id == node.node_id, self.ui_buttons_list))[0]
        temp_node.setText(f'Элемент{node.node_id}: {node.p}')
        self.update()

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
        ids_existing_nodes = []
        for node in self.nodes_list:
            ids_existing_nodes.append(node.node_id)
        for n_id in ids_existing_nodes:
            self.delete_node(n_id)

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

    modal_closed = QtCore.pyqtSignal(Node)

    def __init__(self, dataset: dict):
        super(Modal, self).__init__()
        self.something = ''
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.save_btn.clicked.connect(self.save)
        self.dataset = dataset
        self.fill_data(dataset)

    def fill_data(self, dataset: dict):
        """ """
        nodes_list = dataset.get('nodes_list')

        for node in nodes_list:
            if node.node_id == dataset.get('node_id'):
                self.our_node = node

        self.ui.p_le.setText(str(self.our_node.p))
        if self.our_node.input_node:
            self.ui.input_chb.setChecked(True)
        if self.our_node.output_node:
            self.ui.output_chb.setChecked(True)

    def save(self):
        """ """

        p = self.ui.p_le.text()
        rel = self.ui.lineEdit.text()
        input  = self.ui.input_chb.checkState()
        output = self.ui.output_chb.checkState()

        self.our_node.p = float(self.ui.p_le.text())
        if rel:
            self.our_node.next_nodes = list(map(lambda x: int(x), rel.split(', ')))
        else:
            self.our_node.next_nodes = []
        self.our_node.input_node = input
        self.our_node.output_node = output

        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        """ event after closing of window """

        self.modal_closed.emit(self.our_node)


app = QtWidgets.QApplication([])
application = Start()
application.show()

sys.exit(app.exec())
