from __future__ import print_function
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from itertools import count


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

	def get_value(self):
		# type: () -> object
		return self.value

	def get_hooks(self):
		return self.hooks

	def get_param(self):
		return self.param

	def __eq__(self, other):
		if self.get_value() == other.get_value():
			result = True
		else:
			result = False
		return result

	def __str__(self):
		return ': '.join([str(self.id),str(self.value)])


class Hook(object):
	_ids = count(0)

	def __init__(self):
		self.id = self._ids.next()
		self.nodes = []
		# node.set_hook(node):

	def get_nodes(self):
		return self.nodes

	def capture_node(self, node):
		# print('Capture node: ', node.id)
		self.nodes.append(node)
		node.set_hook(self)

	# def reduce(self, other):
	# 	if self.node == other.node:
	# 		self.node.appeng(other.node)
	# 		other.node.set_hook(self)


class HookCluster(object):
	def __init__(self, hooks=[]):
		self.hooks = hooks

	def create_hook(self):
		hook = Hook()
		self.hooks.append(hook)
		# print('Hook Id: ', hook.id)
		return hook

	def get_hooks(self):
		return self.hooks
	# def __str__(self):
	# 	print_out = ''
	# 	if self.hooks:
	# 		print_out = ', '.join([str(hook) for hook in self.hooks])
	# 	return



class ParamCluster(object):
	def __init__(self, params=[]):
		self.params = params

	def add_param(self, label):
		param = Param(label)
		self.params.append(param)
		return param

	def get_last_param(self):
		return self.params[-1]

	def __str__(self):
		print_out = ''
		if self.params:
			print_out = ', '.join([str(param) for param in self.params])
		return print_out

	def __iter__(self):
		return iter(self.params)

	def get_param(self, label):
		result_label = None
		if self.params:
			for param in self.params:
				if param.get_label() == label:
					result_label = param
		if not result_label:
			raise ValueError
		return result_label

	# def reduce(self):
	# 	for param in self.params:
	# 		param_next_list = self.params[:]
	# 		param_next_list.remove(param)
	# 		# TODO: if node in param also reduced, is it affect list iterating
	# 		if param_next_list:
	# 			for param_next in param_next_list:
	# 				param.reduce(param_next)


class Param(object):
	def __init__(self, label=''):
		self.label = label
		self.nodes = []

	def add_node(self, node):
		self.nodes.append(node)
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
				if node.get_value() == value:
					result_node = node
		if not result_node:
			raise ValueError
		return result_node

	def unique(self):
		dnodes = {node.get_value(): node for node in self.nodes}
		snodes = set(dnodes.keys())
		unique_nodes = []
		for i in snodes:
			unique_nodes.append(dnodes[i])
		self.nodes = unique_nodes



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
		self.node_list = []
		self.param_cluster = ParamCluster()
		self.hook_cluster = HookCluster()
		self.node_list = self.map_to_associative_graph(frame, self.param_cluster)
		self.reduce_nodes()
		self.capture_nodes()

	def map_to_associative_graph(self, frame, param_cluster):
		# print('map_to_associative_graph')
		node_list = []

		if type(frame) == Series:
			row = frame.shape
			column = 1
		elif type(frame) == DataFrame:
			row, column = frame.shape
		# print(param_cluster)
		if column == 1:
			# print(frame.name)
			param_cluster.add_param(frame.name)
			for index, value in frame.iteritems():
				# print(index, value)
				node = Node(value)
				node_list.append(node)
				param_cluster.get_last_param().add_node(node)
				# print(param_cluster)
		else:
			# counter = 0
			for column in frame:
				# print(column)
				# print(counter)
				# counter += 1
				node_list.append(self.map_to_associative_graph(frame=frame[column], param_cluster=param_cluster))
		return node_list

	def reduce_nodes(self):
		for param in self.param_cluster:
			param.unique()

	def capture_nodes(self):
		for index, row in self.frame.iterrows():
			# print(index, row)
			# print('_'*15)
			hook = self.hook_cluster.create_hook()
			for name, cell_value in row.iteritems():
				param = self.param_cluster.get_param(name)
				# print(param, cell_value)
				# for node in param.get_nodes():
				# 	print(node)
				node = param.get_node(cell_value)
				hook.capture_node(node)


if __name__ == "__main__":
	randn = [[1, 1, 1, 1, 2, 2, 2, 3], list('aghjjgla')]  # np.random.rand(10)
	print('*' * 50)
	iris = pd.read_excel('IrisDataAll.xls')
	frame = iris#.ix[:, ['leaf-length','leaf-width']].head(20)
	# print(randn)
	# frame = DataFrame(np.array(randn).transpose(), columns=['Col1', 'Col2'])
	print(frame)
	node_list = []
	hook_list = []

	agds = AssociativeGraph(frame=frame)

	print('\n'*2)
	print('Hook cluster')
	print('Len: ', len(agds.hook_cluster.hooks))
	for hook in agds.hook_cluster.get_hooks():
		# print('^'*50)
		print('Hook Id: ', hook.id)
		# print('\t'*2, len(hook.get_nodes()))
		for node in hook.get_nodes():
			print('\tNode Id: ', node.id, node.get_param(), node.get_value())

	print('\n'*2)
	print('Param cluster')
	print('Len: ', len(agds.param_cluster.params))
	for param in agds.param_cluster:
		print(param)
		print(len(param.get_nodes()))
		for node in param.get_nodes():
			print(node)

	print('\n'*2)
	print('Nodes per params')
	for param in agds.param_cluster.params:
		print(param, len(param.get_nodes()))

	# print('\n'*2)
	# print('Nodes per hook')
	# for hook in agds.hook_cluster.get_hooks():
	# 	print(len(hook.get_nodes()))
	exit(0)

	# for value in frame:
	#     node_list.append(Node(value))

	def map_to_associative_graph(frame, param_cluster):
		# print('map_to_associative_graph')
		node_list = []

		if type(frame) == Series:
			row = frame.shape
			column = 1
		elif type(frame) == DataFrame:
			row, column = frame.shape
		# print(param_cluster)
		if column == 1:
			# print(frame.name)
			param_cluster.add_param(frame.name)
			for index, value in frame.iteritems():
				# print(index, value)
				node = Node(value)
				node_list.append(node)
				param_cluster.get_last_param().add_node(node)
				# print(param_cluster)

		else:
			counter = 0
			for column in frame:
				# print(counter)
				counter += 1
				node_list.append(map_to_associative_graph(frame=frame[column], param_cluster=param_cluster))
		return node_list


	param_cluster = ParamCluster()
	# param_cluster.alloc_param_cluster(3)
	# print(param_cluster.params)
	# exit(0)
	# print(param_cluster)
	hook_cluster = HookCluster()

	node_list = map_to_associative_graph(frame=frame, param_cluster=param_cluster)
	# print(node_list)
	# print(param_cluster)


	# param_cluster.reduce()
	# print('*' * 50)
	for param in param_cluster:
		param.unique()
		# for node in param.get_nodes():
			# print(node)


	# print(param_cluster.get_param(label='Col1').get_node(value=3))
	# def hook_capturing(param_cluster, frame):
	# 	pass

	for index, row in frame.iterrows():
		hook = hook_cluster.create_hook()
		# print(hook.id)
		for name, cell_value in row.iteritems():
			# print('\n')
			# print(name, cell_value)
			param = param_cluster.get_param(name)
			# print(param)
			node = param.get_node(cell_value)
			# print(node)
			hook.capture_node(node)
			# print(hook)
		# print(hook.nodes)
		# print(len(hook.nodes))

	# print('*'*100)
	# print(len(hook_cluster.hooks))
	print('\n'*2)
	print('Hook cluster')
	print('Len: ', len(hook_cluster))
	for hook in hook_cluster.get_hooks():
		# print('^'*50)
		print('Hook Id: ', hook.id)
		# print('\t'*2, len(hook.get_nodes()))
		for node in hook.get_nodes():
			print('\tNode Id: ', node.get_param(), node.get_value())
			# for node in hook.get_nodes():
			# 	print('\t','^'*5)
			# 	print(node)

	print('\n'*2)
	print('Param cluster')
	print('Len: ', len(param_cluster))
	for param in param_cluster:
		print(param.get_label())
		for node in param.get_nodes():
			print(node)

	print('\n'*2)
	print('Node list')
	for node in node_list[0]:
		print ('Nood id: ', node.id)
		hooks = node.get_hooks()
		for hook in hooks:
			print('\tHook Id: ', hook.id)


