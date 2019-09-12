from kgdb.jemalloc.Arena import Arena
from kgdb.jemalloc.Chunk import Chunk
from kgdb.jemalloc.Chunkmap import Chunkmap
from kgdb.jemalloc.Tbin import Tbin
from kgdb.jemalloc.Tcache import *
from kgdb.jemalloc.jemalloc_utils import *
from kgdb.jemalloc.Bin_info import Bin_info
from kgdb.utils.CommonUtils import *

# def parse_arena(readmem, arena_addr):
#     content = readmem(arena_addr, 0x11c0)

#     def fetch(offset, size):
#         return content[offset: offset + size]
#     arena = Arena()
#     arena._ind = u32(fetch(0, 4))
#     arena._nthreads = u32(fetch(4, 4))
#     arena._tcache_ql = u64(fetch(0x78, 8))
#     arena._prof_accumbytes = u64(fetch(0x80, 8))
#     arena._dss_prec = u32(fetch(0x88, 4))
#     arena._chunks_dirty = fetch(0x90, 0x50)
#     arena._spare = fetch(0xe0, 0x8)
#     arena._nactive = fetch(0xe8, 0x8)
#     arena._ndirty = fetch(0xf0, 8)
#     arena._npurgatory = fetch(0xf8, 8)
#     arena._runs_avail = fetch(0x100, 0x20)
#     for i in range(28):
#         arena._bins.append(fetch(0x120 + i * 0x98, 0x98))
#     return arena


# def parse_chunk(readmem, addr):
#     CHUNKMASK = 0xffffffffffffffff ^ (0x400 ** 2 - 1)
#     chunkaddr = addr & CHUNKMASK
#     content = readmem(chunkaddr, 0x1000)
#     def fetch(offset, size):
#         return content[offset: offset + size]
#     chunk = Chunk()
#     chunk._arena = u64(fetch(0, 8))
#     chunk._dirty_link = [u64(fetch(8, 8)), u64(fetch(0x10, 8))]
#     chunk._ndirty = u64(fetch(0x18, 8))
#     chunk._nruns_avail = u64(fetch(0x20, 8))
#     chunk._nruns_adjac = u64(fetch(0x28, 8))
#     for i in range(0x100):
#         chunk._map.append(parse_chunkmap(readmem, addr + 0x28 + 0x18 * i))
#     return chunk
    # TODO parse map


# def parse_chunkmap(readmem, addr):
    # content = readmem(addr, 0x18)

    # def fetch(offset, size):
    #     return content[offset: offset + size]
    # chunkmap = Chunkmap()
    # chunkmap._link[0] = u64(fetch(0, 8))
    # chunkmap._link[1] = u64(fetch(8, 8))
    # chunkmap._bits = u64(fetch(16, 8))
    # return chunkmap

# def parse_arena_list(readmem, arenas_addr):
#     cursor = arenas_addr
#     res = []
#     while True:
#         tmp = u64(readmem(cursor, 8))
#         if tmp == 0:
#             break
#         cursor += 8
#         res.append(tmp)
#     return res