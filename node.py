from itertools import count
import numpy as np


class Node(object):
    _ids = count(0)

    def __init__(self, value):
        self.id = self._ids.next()
        self.value = value
        self.hooks = []
        self.param = ''

    def set_hook(self, hook):
        self.hooks.append(hook)

    def set_param(self, param):
        self.param = param

    def __eq__(self, other):
        if self.get_value() == other.get_value():
            result = True
        else:
            result = False
        return result

    def mark_similar(self, precision, inspected):
        neighbours = [node for node in self.param.nodes if self.probability(node) <= precision]
        for node in neighbours:
            if node.hooks:
                for hook in node.hooks:
                    if not (hook is inspected):
                        hook.similarity += self.distance_btw(node)

    def distance_btw(self, other):
        distance = 0
        # print(type(self.value))
        if not isinstance(self.value, unicode):
            distance = 1 - np.abs(self.value - other.value) / self.param.range

        return distance

    def probability(self, other):
        return np.abs(self.value - other.value) / self.param.range
    def __str__(self):
        return ': '.join([str(self.id), str(self.value)])