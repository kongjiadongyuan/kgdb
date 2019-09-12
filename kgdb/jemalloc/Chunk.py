class Chunk:
    def __init__(self):
        self._arena = None 
        self._dirty_link = None 
        self._ndirty = None 
        self._nruns_avail = None 
        self._nruns_adjac = None 
        self._map = []