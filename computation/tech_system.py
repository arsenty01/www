import random
from typing import List
from node import Node


class TechSystem:

    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.input_nodes = list(filter(lambda x: x.input_node, self.nodes))
        self.output_nodes = list(filter(lambda x: x.output_node, self.nodes))
        self.way = []

    def logic_method(self):
        """Вычисляет с помощью логико-вероятностного метода"""

        truth_table = self.complete_truth_table()
        probability = 0

        for key, value in truth_table.items():
            if value:
                probability += self.calculate_way_probability(self.str_to_list(key))
        return probability

    def statistic_method(self, count: int):
        """Статистический метод"""

        success = 0

        for i in range(count):
            active_nodes = self.random_active_nodes()
            if self.check_way(active_nodes):
                success += 1

        return round(success/count, 6)

    def check_way(self, active_nodes: List[int]):
        """Проверяет, работоспособна ли система
        :param active_nodes: список активных элементов системы
        """
        used_nodes = self.find_way(self.input_nodes, [], active_nodes)
        if not self._check_ports(used_nodes):
            return False
        return True

    def _check_ports(self, active_nodes: List[int]):
        """Проверяет вхождение входных и выходных элементов в список активных"""
        input_is_active = False
        for node in self.input_nodes:
            input_is_active = input_is_active or node.node_id in active_nodes
        output_is_active = False
        for node in self.output_nodes:
            output_is_active = output_is_active or node.node_id in active_nodes
        return output_is_active and input_is_active

    def find_way(self, next_nodes, used_nodes, active_nodes):
        """Поиск и добавление в связанные """
        for node in next_nodes:
            if node.node_id in active_nodes and node.node_id not in used_nodes:
                used_nodes.append(node.node_id)
                used_nodes = self.find_way(node.next_nodes, used_nodes, active_nodes)
        return used_nodes

    def get_node(self, node_id: int):
        return list(filter(lambda x: x.node_id == node_id, self.nodes))[0]

    def calculate_way_probability(self, way: List[int]):
        """Расчёт вероятности с данными активными элементами"""

        result = 1

        for node in self.nodes:
            if node.node_id in way:
                result *= node.p
            else:
                result *= node.q
        return result

    def complete_truth_table(self):
        """Заполняет таблицу истинности нулями и еденицами"""
        truth_table = dict()
        n = len(self.nodes)
        for i in range(2**n):
            active_nodes = self.int_to_list(i, n)
            res = self.check_way(active_nodes)
            key = self.list_to_str(active_nodes)
            truth_table[key] = res
        return truth_table

    def random_active_nodes(self):
        """Рандомно задаёт активные элементы на основе вероятности активности каждого узла"""
        active_nodes = []

        for node in self.nodes:
            rnd = random.random()
            if rnd <= node.p:
                active_nodes.append(node.node_id)

        return active_nodes

    @staticmethod
    def list_to_str(tmp: List[int]):
        """Преобразует лист в строку"""
        return ','.join(map(lambda x: str(x), tmp))

    @staticmethod
    def str_to_list(tmp: str):
        """Преобразует строку в лист"""
        return list(map(lambda x: int(x), tmp.split(',')))

    @staticmethod
    def int_to_list(binary: int, size: int):
        """Преобразует число в список активных элементов"""

        active_nodes = []
        tmp = bin(binary)[2:].zfill(size)
        for index, symbol in enumerate(tmp):
            if int(symbol):
                active_nodes.append(index + 1)
        return active_nodes


