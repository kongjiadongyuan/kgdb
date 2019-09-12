from kgdb.jemalloc.jemalloc_utils import *

class Bitmap_info:
    def __init__(self, content):
        def fetch(offset, size):
            return content[offset: offset + size]
        self._nbits = u64(fetch(0, 8))
        self._nlevels = u32(fetch(8, 4))
        self._levels = []
        self._levels.append(u64(fetch(0x10, 8)))
        self._levels.append(u64(fetch(0x18, 8)))
        self._levels.append(u64(fetch(0x20, 8)))
        self._levels.append(u64(fetch(0x28, 8)))
        self._levels.append(u64(fetch(0x30, 8)))
    
class Bin_info:
    def __init__(self, bin_info_content):
        # self._reg_size = 0
        # self._redzone_size = 0 
        # self._reg_interval = 0 
        # self._run_size = 0
        # self._nregs = 0
        # self._bitmap_offset = 0
        # self._bitmap_info = Bitmap_info()
        # self._reg0_offset = 0
        def fetch(offset, size):
            return bin_info_content[offset: offset + size]
        self._reg_size = u64(fetch(0, 8))
        self._redzone_size = u64(fetch(8, 8))
        self._reg_interval = u64(fetch(0x10, 8))
        self._run_size = u64(fetch(0x18, 8))
        self._nregs = u32(fetch(0x20, 4))
        
        self._bitmap_offset = u32(fetch(0x24, 4))
        self._bitmap_info = Bitmap_info(fetch(0x28, 0x38))
        self._ctx0_offset = u32(fetch(0x60, 4)) 
        self._reg0_offset = u32(fetch(0x64, 4))
    
    def __str__(self):
        res = ''
        res += 'reg_size: \t' + hex(self._reg_size) + '\n'
        res += 'redzone_size: \t' + hex(self._redzone_size) + '\n'
        res += 'reg_interval: \t' + hex(self._reg_interval) + '\n'
        res += 'run_size: \t' + hex(self._run_size) + '\n'
        res += 'nregs: \t' + hex(self._nregs) + '\n'
        res += 'bitmap_offset: \t' + hex(self._bitmap_offset) + '\n'
        res += 'reg0_offset: \t' + hex(self._reg0_offset) + '\n'
        return res


class Bin_info_list:
    def __init__(self, readmem, bin_info_list_addr):
        content = readmem(bin_info_list_addr, BIN_COUNT * 0x68)
        def fetch(offset, size):
            return content[offset: offset + size]
        self._list = []
        for idx in range(BIN_COUNT):
            self._list.append(Bin_info(fetch(idx * 0x68, 0x68)))
    def info(self, idx):
        return self._list[idx]
        