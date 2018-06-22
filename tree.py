from atriact import *

class Node:
	def __init__(self, data=(None, None, None, []), parent=None, children=[]):

		self.parent=parent
		self.children=children
		self.I = Inh()
		self.S = Synth()
		(self.I.ptr, self.I.names, self.I.act, self.S.num) = data # attributes

	def add_child(self, child):
		child.parent = self
		self.children.append(child)
		return self

	def set_parent(self, parent):
		self.parent=parent
		return self

# search routines

	#recursive dfs
	def dfs(self, action=None):
		current = self
		# chk action
		if len(current.children)==0:
			return
		else:
			for node in current.children:
				self.dfs(node)

	#upward branch checking from current node to some global root

	def upbranch(self, action=None):
		current =  self
		while current.parent != None:
			#chk action, thn
			current = current.parent
		return


class Tree: # represents a tree/subtree
	def __init__(self, root=Node()):
		self.root = root

#recursive dfs
	def dfs(self, root=None, action=None):
		if not root:
			root = self.root
		current = root

		# chk action
		if len(current.children)==0:
			return
		else:
			for node in current.children:
				self.dfs(node)
			
#upward branch checking from current root to some global root

	def upbranch(self, action=None):
		while self.root.parent != None:
			#chk action, thn
			self.root = self.root.parent
		return


