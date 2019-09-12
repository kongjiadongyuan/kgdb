from kgdb.jemalloc.jemalloc_utils import *
from kgdb.jemalloc.Freelist import Freelist
class Tbin:
    def __init__(self, readmem, tbin_content, size):
        # self._tstats = None 
        # self._low_water = None 
        # self._lg_fill_div = None 
        # self._ncached = None 
        # self._avail = []
        content = tbin_content
        def fetch(offset, size):
            return content[offset: offset + size]
        self._size = size
        self._tstats = u64(fetch(0, 8))
        self._low_water = u32(fetch(8, 4))
        self._lg_fill_div = u32(fetch(12, 4))
        self._ncached = u64(fetch(16, 8))
        self._avail = []
        avail_addr = u64(fetch(24, 8))
        content = readmem(avail_addr, 8 * (self._ncached))
        for i in range(self._ncached):
            self._avail.append(u64(fetch(i * 8, 8)))
    
    def freelist(self):
        fl = Freelist() 
        fl.add(self._size, self._avail)
        return fl