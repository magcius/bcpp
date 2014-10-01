
import struct
import sys

def lw(f):
    x = f.read(4)
    return struct.unpack('<L', x)[0]

f = open(sys.argv[1], 'rb')

magic = f.read(4)
assert magic == 'AFS\0'

n_files = lw(f)

for i in xrange(n_files):
    name = 'file_%04d' % (i, )
    offs = lw(f)
    size = lw(f)
    print name, offs, size

