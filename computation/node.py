
class Node:

    def __init__(self, p: float, input_node: bool, output_node: bool, node_id: int):
        assert 0 <= p <= 1, 'Вероятность работоспособности элемента должна быть от 0 до 1'
        self.p = p
        self.q = 1-p
        self.input_node = input_node
        self.output_node = output_node
        self.next_nodes = []
        self.node_id = node_id

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