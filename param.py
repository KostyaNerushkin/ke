from __future__ import print_function
from utils import ComponentError
from node import NodeError


class ParamError(ComponentError):
    pass


class NotMeasurableParamError(ParamError):
    pass


class Param(object):

    def __init__(self, name=''):
        self.name = name
        self.nodes = []
        self.range = 0

    def append(self, node):
        self.nodes.append(node)
        print()
        self.reduce()
        try:
            self.measure()
        except NotMeasurableParamError:
            pass
        node.param = self

    def node(self, by_value):
        result_node = None
        if self.nodes:
            for node in self.nodes:
                if node.value == by_value:
                    result_node = node
        else:
            raise ParamError('No nodes defined')
        if not result_node:
            raise NodeError('Node with ' + str(by_value) + ' not in ' + self.name)
        return result_node

    def reduce(self):
        dict_nodes = {node.value: node for node in self.nodes}
        set_nodes_values = set(dict_nodes.keys())
        unique_nodes = []
        for node in set_nodes_values:
            unique_nodes.append(dict_nodes[node])
        self.nodes = unique_nodes
        self.nodes.sort(key=lambda x: x.value, reverse=False)

    def measure(self):
        if isinstance(self.nodes[0].value, float):
            self.range = self.nodes[-1].value - self.nodes[0].value
        else:
            raise NotMeasurableParamError('Not measurable param')


    def __str__(self):
        return self.name

    def __iter__(self):
        return iter(self.nodes)