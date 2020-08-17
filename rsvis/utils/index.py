# ===========================================================================
#   index.py ----------------------------------------------------------------
# ===========================================================================

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class Index:

    #   method --------------------------------------------------------------
    # ----------------------------------------------------------------------- 
    def __init__(self, limit, start=0):
        self._index = start
        self._start = start
        self._limit = limit

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __call__(self, index=None):
        if index is not None:
            self._index=index
        return self.index
  
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __iter__(self):
        self.index = -1

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __next__(self):
        if self.index == len(self)-1:
            raise StopIteration
        
        self._index += 1
        
        return self
    
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __eq__(self, obj):
        if isinstance(obj, Index):
            return self.index == obj.index and self.limit == self.limit and self.__len__ == len(obj) 

        return False

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------  
    def __ne__(self, obj):
        return not self.__eq__(obj)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __len__(self):
        return self._limit - self._start

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def next(self):
        self._index += 1
        if self._index == self._limit:
            self._index = self._start
        return self._index
        
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def last(self):
        self._index -= 1
        if self._index == self._start-1:
            self._index = self._limit-1
        return self._index

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __add__(self, value):
        for i in range(value):
            self.next()
        return self

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------  
    def __sub__(self, value):
        for i in range(value):
            self.last()
        return self

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __iadd__(self, value):
        self.__add__(value)
        return self

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------  
    def __isub__(self, value):
        self.__sub__(value)
        return self

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------  
    def append(self, value):
        self._limit += value

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------  
    def end(self):
        self._index = self._limit-1

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @property
    def index(self):
        return self._index

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @index.setter
    def index(self, index):
        self._index = index

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @property
    def limit(self):
        return self._limit

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    @limit.setter
    def limit(self, limit):
        self._limit = limit

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __repr__(self):
        return "<Index '{}' with limit {}>".format(self.index, self.limit)