
class Node:

    def __init__(self, p: float, input_node: bool, output_node: bool, node_id: int, x1: int, y1: int):
        assert 0 <= p <= 1, 'Вероятность работоспособности элемента должна быть от 0 до 1'
        self.p = p
        self.q = 1-p
        self.input_node = input_node
        self.output_node = output_node
        self.next_nodes = []
        self.node_id = node_id
        self._x1 = x1
        self._y1 = y1

    @property
    def get_coordinates(self) -> tuple:
        """
            Получаем текущие координаты

        :return: координаты
        """
        return self._x1, self._y1

    def set_coordinates(self, x1, y1):
        """
            Задаем координаты ноды

        :param x1:
        :param y1:
        :return:
        """

        self._x1 = x1
        self._y1 = y1

    def get_center(self) -> tuple:
        """ """

        return self._x1+45, self._y1+20

    def add_next_node(self, new_node: object):
        """
        Связывает два элемента
        :param self: текущий элемент
        :param new_node: следующий элемент
        """

        assert isinstance(new_node, Node), 'Следующими элементами могут быть только экземпляры класса элемента (Node)'
        self.next_nodes.append(new_node)

    def __repr__(self):
        next_ids = []
        if self.next_nodes:
            next_ids = list(map(lambda x: x.node_id, self.next_nodes))
        return f'Элемент с номером {self.node_id}. Номера связанных элементов - {next_ids}'