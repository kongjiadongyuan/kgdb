import struct


sztable = [0x8,
           0x10,
           0x20,
           0x30,
           0x40,
           0x50,
           0x60,
           0x70,
           0x80,
           0xa0,
           0xc0,
           0xe0,
           0x100,
           0x140,
           0x180,
           0x1c0,
           0x200,
           0x280,
           0x300,
           0x380,
           0x400,
           0x500,
           0x600,
           0x700,
           0x800,
           0xa00,
           0xc00,
           0xe00,
           0x1000,
           0x2000,
           0x3000, 
           0x4000, 
           0x5000, 
           0x6000, 
           0x7000, 
           0x8000]

BIN_COUNT = 28
TBIN_COUNT = 36


def p64(num):
    return struct.pack("<Q", num)


def u64(content):
    if not len(content) == 8:
        raise Exception("u64 should accept buffer with length 8.")
    return struct.unpack("<Q", content)[0]


def p32(num):
    return struct.pack("<I", num)


def u32(content):
    if not len(content) == 4:
        raise Exception("u32 should accept buffer with length 4.")
    return struct.unpack("<I", content)[0]


def size2bin(sz):
    for i in range(len(sztable)):
        if sz <= sztable[i]:
            return i
    return -1


def bin2size(binidx):
    return sztable[binidx]

def map2run(addr): 
    offsetmask = (0x400 * 0x400 * 4 - 1)
    chunkmask = 0xffffffffffffffff ^ offsetmask
    chunkaddr = addr & chunkmask
    mapoffset = addr & offsetmask
    mapidx = int((mapoffset - 0x30) / 0x18)
    runaddr = chunkaddr + 0x1000 * (mapidx + 6)
    return runaddr


if __name__ == '__main__':
    pass