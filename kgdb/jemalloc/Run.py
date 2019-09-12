from kgdb.jemalloc.jemalloc_utils import *
from kgdb.jemalloc.Freelist import *


class Run:
    def __init__(self, readmem, addr, bin_info):
        self._reg_size = bin_info._reg_size
        self._addr = addr
        regbase = bin_info._reg0_offset + addr
        nreg = bin_info._nregs
        if nreg % 8 == 0:
            bitmaplen = int(nreg / 8)
        else:
            bitmaplen = int(nreg / 8) + 1
        bitmapbase = bin_info._bitmap_offset
        content = readmem(addr, bitmapbase + bitmaplen)

        def fetch(offset, size):
            return content[offset: offset + size]
        self._bin = u64(fetch(0, 8))
        self._nextind = u32(fetch(8, 4))
        self._nfree = u32(fetch(12, 4))
        bitmap = fetch(bitmapbase, bitmaplen)
        freeidx = []
        for idx in range(nreg):
            byteidx = int(idx / 8)
            bitidx = idx % 8
            probe = 1 << bitidx
            tmp = bitmap[byteidx]
            if type(tmp) == str:
                tmp = ord(tmp)
            elif type(tmp) == int:
                pass
            else:
                raise Exception("Compatibility......")
            if(tmp & probe):
                freeidx.append(idx)
        self._free_reg_list = []
        for idx in freeidx:
            self._free_reg_list.append(regbase + idx * self._reg_size)

    def freelist(self):
        fl = Freelist()
        fl.add(self._reg_size, self._free_reg_list)
        return fl
