from kgdb.jemalloc.jemalloc_utils import *
from kgdb.jemalloc.Freelist import Freelist
from kgdb.jemalloc.Tbin import *

class Tcache:
    def __init__(self, readmem, tcache_addr):
        # self._addr = 0
        # self._link = [0, 0]
        # self._prof_accumbytes = None
        # self._arena = None
        # self._ev_cnt = None
        # self._next_gc_bin = None
        # self._tbins = []
        # for _ in range(TBIN_COUNT):
            # self._tbins.append(None)
        content = readmem(tcache_addr, 0x28 + 0x20 * TBIN_COUNT)
        def fetch(offset, size):
            return content[offset: offset + size]
        self._addr = tcache_addr
        self._link = [0, 0]
        self._link[0] = u64(fetch(0, 8))
        self._link[1] = u64(fetch(8, 8))
        self._prof_accumbytes = u64(fetch(0x10, 8))
        self._arena = u64(fetch(0x18, 8))
        self._ev_cnt = u32(fetch(0x20, 4))
        self._next_gc_bin = u32(fetch(0x24, 4))
        self._tbins = []
        for _i in range(TBIN_COUNT):
            self._tbins.append(Tbin(readmem, fetch(0x28 + 0x20 * _i, 0x20), bin2size(_i)))
    
    def freelist(self):
        fl = Freelist()
        for idx in range(len(self._tbins)):
            fl += self._tbins[idx].freelist()
        return fl