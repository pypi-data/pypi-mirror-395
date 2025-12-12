"""Efficient implementation of immutable sets using bit vectors"""
from itertools import combinations


class BitVectorSet(int):
    """Immutable sets over {0,...,n}"""

    def __new__(cls, iterable=()):
        x = 0
        for i in iterable:
            x = x | 1<<int(i)
        return super(BitVectorSet, cls).__new__(cls, x)
    
    @classmethod
    def from_int(cls, x : int):
        if x < 0:
            raise ValueError("BitVectorSet.from_int(x): x should be a non-negative integer")
        return super(BitVectorSet, cls).__new__(cls, x)

        
    
    def __len__(self):
        return self.bit_count()
    
    def __contains__(self, i):
        return (self>>i)&1 == 1
    
    def __iter__(self):
        x, i = self, 0
        while x > 0:
            if int.__and__(x,1) == 1:
                yield i
            i+=1
            x>>=1

    def __eq__(self, other):
        return self.__class__ == other.__class__ and int.__eq__(self, other)

    def isdisjoint(self, other):
        """Return True if the set has no elements in common with other. 
        
        Sets are disjoint if and only if their intersection is the empty set"""
        return self & other != 0
    
    def issubset(self, other):
        """Test whether every element in the set is in other."""
        return self & other == self
    
    def __le__(self, other):
        """Test whether every element in the set is in other."""
        return self.issubset(other)
    
    def issuperset(self, other):
        """Test whether every element in other is in the set."""
        return other.issubset(self)
    
    def __ge__(self, other):
        """Test whether every element in other is in the set."""
        return self.issuperset(other)
    
    def __or__(self, other):
        """Return a new set with elements from the set and the other."""
        return self.__class__.from_int(int.__or__(self,other))
    
    def union(self, *others):
        """Return a new set with elements from the set and all others."""
        if len(others)==0:
            return self
        return (self|others[0]).union(*others[1:])
    
    def __and__(self, other):
        """Return a new set with elements common to the set and the other."""
        return self.__class__.from_int(int.__and__(self, other))
    
    def intersection(self, *others):
        """Return a new set with elements common to the set and all others."""
        if len(others)==0:
            return self
        return (self&others[0]).intersection(*others[1:])
    
    def __sub__(self, other):
        """Return a new set with elements in the set that are not in the other."""
        return self.__class__.from_int(int.__sub__(self, other&self))
    
    def difference(self, *others):
        """Return a new set with elements in the set that are not in the others."""
        if len(others)==0:
            return self
        return (self-others[0]).difference(*others[1:])
    
    def __xor__(self, other):
        """Return a new set with elements in either the set or other but not both."""
        return self.__class__.from_int(int.__xor__(self, other))
    
    def symmetric_difference(self, other):
        """Return a new set with elements in either the set or other but not both."""
        return self^other
    
    def __repr__(self):
        #return self.__class__.__name__ + "(" + ", ".join((str(i) for i in self)) + ")"
        return self.__class__.__name__ + "(" + int.__repr__(self) + ")"
    
    def __str__(self):
        return "{" + ", ".join((str(i) for i in self)) + "}"
    
    def __hash__(self):
        return int.__hash__(self)

BitVectorSet.EMPTYSET = BitVectorSet.from_int(0)



class IndexedBitVectorSet(BitVectorSet):

    FOD = []
    FODinv = {}

    @staticmethod
    def get_index(element):
        try:
            return IndexedBitVectorSet.FODinv[element]
        except KeyError:
            IndexedBitVectorSet.FOD.append(element)
            index = len(IndexedBitVectorSet.FOD)-1
            IndexedBitVectorSet.FODinv[element] = index
            return index

    def __new__(cls, iterable=()):
        x = 0
        for el in iterable:
            i = IndexedBitVectorSet.get_index(el)
            x = x | 1<<i
        return super(BitVectorSet, cls).__new__(cls, x)

    def __contains__(self, el):
        i = IndexedBitVectorSet.get_index(el)
        return (self>>i)&1 == 1
    
    def __iter__(self):
        x, i = int(self), 0
        while x > 0:
            if x & 1 == 1:
                yield IndexedBitVectorSet.FOD[i]
            i+=1
            x>>=1
    
    def __hash__(self):
        return int.__hash__(self)

IndexedBitVectorSet.EMPTYSET = IndexedBitVectorSet.from_int(0)




def iter_subsets(A, k=None, cls=frozenset):
    """
    Iterator over subsets of A
    
    :param A: Superset
    :param k: size of subsets, or None
    :param cls: Class for sets
    """
    if k is None:
        for k in range(0, len(A)+1):
            for B in iter_subsets(A, k, cls):
                yield B
    else:
        for x in combinations(A, k):
            yield cls(x)





# Some tests
if __name__ == "__main__":

    A = BitVectorSet([0,3,5,6])
    A2 = BitVectorSet.from_int(105)
    B = BitVectorSet((10,))
    C = BitVectorSet((3,1000))


    print("A =", A, "=", int(A))
    print("C =", C, "=", int(C))
    print(A & C, A | C, A - C, A ^ C)



    A = IndexedBitVectorSet(["abc", 7, (1,2,3)])
    C = IndexedBitVectorSet([0, 78, (1,2,3), IndexedBitVectorSet.EMPTYSET, BitVectorSet.EMPTYSET, A])

    print("A =", A, "=", int(A))
    print("C =", C, "=", int(C))
    print(A & C, A | C, A - C, A ^ C)
    print(IndexedBitVectorSet.FOD, IndexedBitVectorSet.FODinv)