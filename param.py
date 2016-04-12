class Param(object):
    def __init__(self, label=''):
        self.label = label
        self.nodes = []
        self.range = 0

    def add_node(self, node):
        self.nodes.append(node)
        # TO DO: Add range updating on the fly, when node is added
        # self.update_range()
        node.set_param(self)

    def get_nodes(self):
        return self.nodes

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def __str__(self):
        return self.label

    def __iter__(self):
        return iter(self.nodes)

    # def __next__(self):

    def get_node(self, value):
        result_node = None
        if self.nodes:
            for node in self.nodes:
                if node.value == value:
                    result_node = node
        if not result_node:
            raise ValueError
        return result_node

    def unique(self):
        dnodes = {node.value: node for node in self.nodes}
        snodes = set(dnodes.keys())
        unique_nodes = []
        for i in snodes:
            unique_nodes.append(dnodes[i])
        self.nodes = unique_nodes
        self.nodes.sort(key=lambda x: x.value, reverse=False)
        self.update_range()

    def update_range(self):
        if isinstance(self.nodes[0].value, float):
            self.range = self.nodes[-1].value - self.nodes[0].value
        else:
            self.range = None