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
	def dfs(self, action=action_check_attr, **kwargs):
		current = self
		chk, current = action(current, **kwargs)
		if chk:
			return (chk, current)
		
		if len(current.children)==0:
			return (chk, current)
		else:
			for node in current.children:
				(chk, crnt) = self.dfs(node)
				if chk:
					return (chk, crnt) # ret from recursion

	#upward branch checking from current node to some global root

	def upbranch(self, action=action_check_attr, **kwargs):
		chk, current =  False, self
		while current.parent != None:
			chk, current = action(current, **kwargs)
			if chk:
				break
			current = current.parent
		return (chk, current)


class Tree: # represents a tree/subtree
	def __init__(self, root=Node()):
		self.root = root

#recursive dfs
	def dfs(self, root=None, action=None, **kwargs):
		if not root:
			root = self.root
		current = root
                chk, current = action(current, **kwargs)
		if chk:
			return (chk, current)

		if len(current.children)==0:
			return (chk, current)
		else:
			for node in current.children:
				(chk, crnt) = self.dfs(node)
				if chk:
					return (chk, crnt)
			
#upward branch checking from current root to some global root

	def upbranch(self, bottom=None ,action=None, **kwargs):
		chk, current = False, self.root
		if bottom:
			current = bottom
		while current.parent != None:
			chk, current = action(current, **kwargs)
			current = current.parent
		return


