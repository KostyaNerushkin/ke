from __future__ import print_function
from itertools import count
import numpy as np

class Hook(object):
    _ids = count(0)

    def __init__(self):
        self.id = self._ids.next()
        self.nodes = []
        self.similarity = []

    # node.set_hook(node):

    def get_nodes(self):
        return self.nodes

    def get_node_by_param(self, param):
        result = None
        for node in self.nodes:
            if node.param == param:
                result = node
        return result

    def capture_node(self, node):
        # print('Capture node: ', node.id)
        self.nodes.append(node)
        node.set_hook(self)

    def get_similar(self, precision):
        for node in self.nodes:
            node.mark_similar(precision=precision, inspected=self)
        # self.nodes[0].mark_similar(precision, self)
        #
        # print('Node', self.nodes[len(self.nodes) - 1])
    # def reduce(self, other):
    # 	if self.node == other.node:
    # 		self.node.appeng(other.node)
    # 		other.node.set_hook(self)

