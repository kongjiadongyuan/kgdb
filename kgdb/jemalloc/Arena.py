from kgdb.jemalloc.jemalloc_utils import *
from kgdb.jemalloc.Bin_info import *
from kgdb.jemalloc.Tcache import *
from kgdb.jemalloc.Bin import *


class Arena:
    def __init__(self, readmem, arena_addr, bin_info_list_addr):
        content = readmem(arena_addr, 0x11c0)
        bin_info_list = Bin_info_list(readmem, bin_info_list_addr)

        def fetch(offset, size):
            return content[offset: offset + size]
        self._ind = u32(fetch(0, 4))
        self._nthreads = u32(fetch(4, 4))
        self._lock = fetch(8, 0x28)
        self._stats = fetch(0x30, 0x48)
        self._tcache_list = []
        tmpaddrlist = []

        def go(tcache_addr):
            if tcache_addr in tmpaddrlist or tcache_addr == 0:
                pass
            else:
                tmpaddrlist.append(tcache_addr)
                tmptcache = Tcache(readmem, tcache_addr)
                self._tcache_list.append(tmptcache)
                go(tmptcache._link[0])
                go(tmptcache._link[1])
        go(u64(fetch(0x78, 8)))
        self._prof_accumbytes = u64(fetch(0x80, 0x8))
        self._dss_prec = u32(fetch(0x88, 4))
        self._chunks_dirty = fetch(0x90, 0x50)
        self._spare = u64(fetch(0xe0, 0x8))
        self._nactive = u64(fetch(0xe8, 0x8))
        self._ndirty = u64(fetch(0xf0, 0x8))
        self._npurgatory = u64(fetch(0xf8, 0x8))
        self._runs_avail = fetch(0x100, 0x20)
        self._bin_list = Bin_list(readmem, fetch(0x120, 0x10a0), bin_info_list)
    
    def freelist(self):
        fl = Freelist()
        fl += self._bin_list.freelist()
        for tcache in self._tcache_list:
            fl += tcache.freelist()
        return fl