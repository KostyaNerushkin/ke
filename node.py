from __future__ import print_function
from itertools import count
import numpy as np
from utils import ComponentError


class NodeError(ComponentError):
    pass

class Node(object):
    _ids = count(0)

    def __init__(self, value):
        self.id = self._ids.next()
        self.value = value
        self.hooks = []
        self.param = ''

    def mark_similar(self, proximity, inspected):
        if isinstance(self.value, float):
            neighbours = [node for node in self.param.nodes if self.neighborhood(node) <= proximity]
            for node in neighbours:
                if node.hooks:
                    for hook in node.hooks:
                        if not (hook is inspected):
                            hook.similarity.append(self.distance(node))

    def distance(self, other):
        dist = 0
        if not isinstance(self.value, unicode):
            dist = 1 - (np.abs(self.value - other.value) / self.param.range)
        return dist

    def neighborhood(self, other):
        print(1 - np.abs(self.value - other.value) / self.param.range)
        return np.abs(self.value - other.value) / self.param.range

    def __eq__(self, other):
        if self.get_value() == other.get_value():
            result = True
        else:
            result = False
        return result

    def __str__(self):
        return ': '.join([str(self.id), str(self.value)])