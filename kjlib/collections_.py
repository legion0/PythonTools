from collections import MutableSet, OrderedDict
import sys

from kjlib.functional import identity_function

def find_in_list(list_, predicate, parser=identity_function, default=None):
	for item in list_:
		if predicate(item):
			return parser(item)
	return default

class HashableOrderedDict(OrderedDict):
	def __hash__(self):
		for key, value in self.iteritems():
			if type(value) is list:
				self[key] = tuple(value)
		return hash(tuple(sorted(self.items())))

class OrderedSet(MutableSet):

	def __init__(self, iterable=None):
		self.end = end = []
		end += [None, end, end]  # sentinel node for doubly linked list
		self.map = {}  # key --> [key, prev, next]
		if iterable is not None:
			self |= iterable

	def __len__(self):
		return len(self.map)

	def __contains__(self, key):
		return key in self.map

	def add(self, key):
		if key not in self.map:
			end = self.end
			curr = end[1]
			curr[2] = end[1] = self.map[key] = [key, curr, end]

	def discard(self, key):
		if key in self.map:
			key, prev, _next = self.map.pop(key)
			prev[2] = _next
			_next[1] = prev

	def __iter__(self):
		end = self.end
		curr = end[2]
		while curr is not end:
			yield curr[0]
			curr = curr[2]

	def __reversed__(self):
		end = self.end
		curr = end[1]
		while curr is not end:
			yield curr[0]
			curr = curr[1]

	def pop(self, last=True):
		if not self:
			raise KeyError('set is empty')
		key = self.end[1][0] if last else self.end[2][0]
		self.discard(key)
		return key

	def __repr__(self):
		if not self:
			return '%s()' % (self.__class__.__name__,)
		return '%s(%r)' % (self.__class__.__name__, list(self))

	def __eq__(self, other):
		if isinstance(other, OrderedSet):
			return len(self) == len(other) and list(self) == list(other)
		return set(self) == set(other)


def __test(argv):
	s = OrderedSet('abracadaba')
	t = OrderedSet('simsalabim')
	print(s | t)
	print(s & t)
	print(s - t)

if __name__ == '__main__':
	__test(sys.argv[1:])
