class Inh:
	def __init__(self, ptrs=None, names=None, act=None):
		self.ptr=ptrs
		self.names=names
		self.act=act

	def __str__(self):
		print('Node inherited attributes')
		print('lists:')
		try:
			print(self.ptr)
		except:
			print('No lists')
		try:
			print(self.names)
		except:
			print('No variables names')
		try:
			print(self.act)
		except:
			print('No syscall recognised')

class Synth:
	def __init__(self, values=[]):
		self.num = values

	def __getitem__(self,key):
		return self.num[key]

	def __setitem__(self,key,value):
		self.num[key] = value

	def __str__(self)
		print(self.num)
