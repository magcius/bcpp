
import os
import json
import struct
import sys
import zipfile
from cStringIO import StringIO

packed_file = sys.argv[1]
in_dir = '%s.d' % (packed_file,)

def align(f):
    N = 2048
    length = f.tell()
    n_zeroes = N - (length % N)
    if n_zeroes < N:
        f.write('\0' * n_zeroes)

def make_packfile(magic, children):
    f = StringIO()
    f.write(magic)

    f.write(struct.pack('<L', len(children)))
    toc = []
    for child in children:
        toc.append((f.tell(), child))
        f.write('\0\0\0\0\0\0\0\0')

    for toc_entry, child in toc:
        align(f)
        child_data = pack(child).getvalue()
        offs = f.tell()
        size = len(child_data)
        f.write(child_data)
        f.seek(toc_entry, os.SEEK_SET)
        f.write(struct.pack('<LL', offs, size))
        f.seek(0, os.SEEK_END)

    return f

def make_zipfile(child_name, child_data):
    f = StringIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr(child_name, child_data.getvalue())
    z.close()
    return f

def make_data(name):
    path = '%s/%s' % (in_dir, name)
    with open(path, 'rb') as f:
        return StringIO(f.read())

def pack(node):
    name = node['name']
    type = node['type']
    children = node['children']

    if type == 'toplevel':
        assert len(children) == 1
        child = children[0]
        return pack(child)
    elif type in ('AFS\0', 'PACK'):
        return make_packfile(type, children)
    elif type == 'zip':
        assert len(children) == 1
        child = children[0]
        return make_zipfile(child['name'], pack(child))
    elif type == 'data':
        assert len(children) == 0
        return make_data(name)
    else:
        print "Unknown inventory type", type
        assert False

invp = '%s/inventory.json' % (in_dir,)
with open(invp, 'r') as f:
    inv = json.load(f)

with open(packed_file, 'wb') as f:
    data = pack(inv)
    f.write(data.getvalue())
