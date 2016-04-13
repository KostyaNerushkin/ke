from __future__ import print_function
from itertools import count
from utils import ComponentError
import numpy as np

class HookError(ComponentError):
    pass


class Hook(object):
    _ids = count(0)

    def __init__(self):
        self.id = self._ids.next()
        self.nodes = []
        self.similarity = []

    def get_by_param(self, param):
        result = None
        for node in self.nodes:
            if node.param == param:
                result = node
        if not result:
            raise HookError
        return result

    def capture(self, node):
        self.nodes.append(node)
        # Similarity is defined only for quantitative value
        if isinstance(node.value, float):
            self.similarity.append(0)
        node.hooks.append(self)

    def similar(self, proximity):
        for node in self.nodes:
            node.mark_similar(proximity=proximity, inspected=self)

