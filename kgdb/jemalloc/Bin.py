from kgdb.jemalloc.jemalloc_utils import *
from kgdb.jemalloc.Freelist import *
from kgdb.jemalloc.Run import *

def parse_runs(readmem, content):
    def fetch(offset, size):
        return content[offset: offset + size]
    root = u64(fetch(0, 8))
    niladdr = u64(fetch(8, 8))
    maplist = []

    def go(addr):
        if addr in maplist or addr == niladdr or addr == 0:
            pass
        else:
            maplist.append(addr)
            tmpcontent = readmem(addr, 0x10)
            addr1 = u64(tmpcontent[0: 8])
            addr2 = u64(tmpcontent[8: 0x10])
            go(addr1)
            go(addr2)
    go(root)
    runlist = []
    for addr in maplist:
        runlist.append(map2run(addr))
    return runlist


class Bin:
    def __init__(self, readmem, bincontent, bin_info):
        def fetch(offset, size):
            return bincontent[offset: offset + size]
        self._lock = fetch(0, 0x28)
        runcur_addr = u64(fetch(0x28, 8))
        if runcur_addr == 0:
            self._runcur = None
        else:
            self._runcur = Run(readmem, runcur_addr, bin_info)
        runlist = parse_runs(readmem, fetch(0x30, 0x20))
        self._runs = []
        for runaddr in runlist:
            self._runs.append(Run(readmem, runaddr, bin_info))
        self._stats = fetch(0x50, 0x48)
    
    def freelist(self):
        fl = Freelist()
        if self._runcur == None:
            pass
        else:
            fl += self._runcur.freelist()
        for run in self._runs:
            fl += run.freelist()
        return fl


class Bin_list:
    def __init__(self, readmem, bin_list_content, bin_info_list):
        def fetch(offset, size):
            return bin_list_content[offset: offset + size]
        self._list = []
        for i in range(BIN_COUNT):
            self._list.append(Bin(readmem, fetch(i * 0x98, 0x98), bin_info_list.info(i)))
    
    def freelist(self):
        fl = Freelist()
        for ubin in self._list:
            fl += ubin.freelist()
        return fl