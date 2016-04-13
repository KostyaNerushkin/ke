from __future__ import print_function
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from itertools import count
from node import Node
from hook import Hook
from param import Param
from utils import ComponentError

class HookList(object):
    def __init__(self):
        self.hooks = []

    def add(self):
        hook = Hook()
        self.hooks.append(hook)
        # print('Hook Id: ', hook.id)
        return hook

    def verify_similar(self):
        for hook in self.hooks:
            if hook.similarity:
                hook.similarity = np.array(hook.similarity).mean()
            else:
                hook.similarity = 0
    # def __str__(self):
    # 	print_out = ''
    # 	if self.hooks:
    # 		print_out = ', '.join([str(hook) for hook in self.hooks])
    # 	return

class ParamNotExistError(ComponentError):
    pass

class ParamList(object):

    def __init__(self):
        self.params = []

    def add(self, name):
        param = Param(name)
        self.params.append(param)
        return param

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

    # def reduce(self):
    # 	for param in self.params:
    # 		param_next_list = self.params[:]
    # 		param_next_list.remove(param)
    # 		# TODO: if node in param also reduced, is it affect list iterating
    # 		if param_next_list:
    # 			for param_next in param_next_list:
    # 				param.reduce(param_next)

    # def reduce(self):
    # 	for node in self.nodes:
    # 		node_next_list = self.nodes[:]
    # 		node_next_list.remove(node)
    # 		# TODO: if node in param also reduced, is it affect list iterating
    # 		# TODO: need to create unique list, and then assign nodes to hooks
    # 		if node_next_list:
    # 			for node_next in node_next_list:
    # 				if node == node_next:
    # 					node = other.node
    # 					other.node.set_param(self)
    # def reduce(self, other):
    # 	#TODO: Scaling problem when reducing params
    # 	for node in self.nodes:
    # 		if node == other.node:
    # 			node = other.node
    # 			other.node.set_param(self)


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
            param_list.add(frame.name)
            for index, value in frame.iteritems():
                node = Node(value)
                node_list.append(node)
                param_list.index(frame.name).append(node)
        else:
            for column in frame:
                node_list.append(self.transform(frame=frame[column], param_list=param_list))
        return node_list

    def similar_to(self, indexes, proximity):
        for index in indexes:
            self.hook_list.hooks[index].similar(proximity)
            print(self.hook_list.hooks[index])
        self.hook_list.verify_similar()

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
    associative_graph.similar_to([3, 4, 5], proximity=0.1)
    for hook in associative_graph.hook_list.hooks:
        print('\t', 'Similarity: ', hook.similarity, hook.get_by_param(associative_graph.param_list.index('class')).value)

