from __future__ import print_function
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from itertools import count
from node import Node
from hook import Hook, HookError
from param import Param, ParamType
from utils import ComponentError
from operator import attrgetter

class HookList(object):
    def __init__(self):
        self.hooks = []

    def add(self):
        hook = Hook()
        self.hooks.append(hook)
        return hook

    def verify_similar(self, weights):
        for hook in self.hooks:
            if hook.similarity:
                hook.similarity = np.dot(np.array(hook.similarity), weights)
            else:
                hook.similarity = 0


class ParamNotExistError(ComponentError):
    pass


class ParamList(object):

    def __init__(self):
        self.params = []
        self.weights = []

    def add(self, name):
        param = Param(name)
        self.params.append(param)
        return param

    def get_weights(self):
        return  np.array([1 / float(len(self.quantitive()))] * (len(self.quantitive())))

    # TODO: refactor to avoid this function, used to extract quantitive params
    def quantitive(self):
        return [param for param in self.params if param.type == ParamType.quantitative]

    def index(self, name):
        result = None
        for param in self.params:
            if param.name == name:
                result = param
        if not result:
            raise ParamNotExistError
        return result

    def __str__(self):
        print_out = ''
        if self.params:
            print_out = ', '.join([str(param) for param in self.params])
        return print_out

    def __iter__(self):
        return iter(self.params)


class AssociativeGraph(object):
    def __init__(self, frame):
        self.frame = frame
        self.param_list = ParamList()
        self.hook_list = HookList()
        self.nodes_list = self.transform(frame, self.param_list)
        self.reduce_nodes()
        self.capture_nodes()

    def transform(self, frame, param_list):
        node_list = []

        if type(frame) == Series:
            row, column = frame.shape, 1
        elif type(frame) == DataFrame:
            row, column = frame.shape

        if column == 1:
            param = param_list.add(frame.name)
            for index, value in frame.iteritems():
                node = Node(value)
                node_list.append(node)
                param.append(node)
        else:
            for column in frame:
                node_list.append(self.transform(frame=frame[column], param_list=param_list))
        return node_list

    def similarity(self, indexes, proximity=1):
        for index in indexes:
            if index in range(len(self.hook_list.hooks)):
                self.hook_list.hooks[index].similar(proximity)
            else:
                raise HookError
        self.hook_list.verify_similar(self.param_list.get_weights())

    def reduce_nodes(self):
        for param in self.param_list:
            param.reduce()

    def capture_nodes(self):
        for index, row in self.frame.iterrows():
            hook = self.hook_list.add()
            for name, value in row.iteritems():
                param = self.param_list.index(name)
                node = param.node(by_value=value)
                hook.capture(node)


if __name__ == "__main__":
    randn = [[1, 1, 1, 1, 2, 2, 2, 3], list('aghjjgla')]  # np.random.rand(10)
    print('*' * 50)
    iris = pd.read_excel('IrisDataAll.xls')
    frame = iris  # .ix[:, ['leaf-length','leaf-width']].head(20)
    # print(randn)
    # frame = DataFrame(np.array(randn).transpose(), columns=['Col1', 'Col2'])
    print(frame)
    associative_graph = AssociativeGraph(frame=frame)
    associative_graph.similarity([124], proximity=1)
    print(type(associative_graph.hook_list.hooks))
    for hook in sorted(associative_graph.hook_list.hooks,key=attrgetter('similarity')):
        print('\t', 'Similarity: ', hook.similarity, hook.get_by_param(associative_graph.param_list.index('class')).value)
        # for node in hook.nodes:
        #     print('\t', node.value)
    for node in associative_graph.hook_list.hooks[123].nodes:
        print('\t', node.value)