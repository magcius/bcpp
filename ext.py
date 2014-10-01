
import json
import os
import struct
import sys
import zipfile
from cStringIO import StringIO

def lw(f):
    x = f.read(4)
    return struct.unpack('<L', x)[0]

def mkd(p):
    try:
        os.makedirs(p)
    except:
        pass

class Output(object):
    def __init__(self, out_dir):
        self.dir = out_dir
        self.inventory = Invrec('toplevel', 'toplevel')

    def dump(self, name, f):
        path = '%s/%s' % (self.dir, name)
        with open(path, 'wb') as out_f:
            out_f.write(f.read())

    def dump_inv(self):
        # write inventory
        path = '%s/inventory.json' % (self.dir,)
        with open(path, 'wb') as f:
            json.dump(self.inventory.serialize(), f, indent=2, sort_keys=True)

class Invrec(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.children = []

    def serialize(self):
        return dict(name=self.name,
                    type=self.type,
                    children=[c.serialize() for c in self.children])

def extract_toplevel(filename):
    out_dir = '%s.d' % (filename,)

    with open(filename, 'rb') as f:
        mkd(out_dir)
        out = Output(out_dir)
        extract_archive(out, filename, f, out.inventory, check_magic='AFS\0')
        out.dump_inv()

def extract_data(out, name, f, parent_invrec):
    magic = f.read(4)
    f.seek(-4, os.SEEK_CUR)

    raw_types = {
        'NULL': 'null',
        'RIFF': 'wav',
    }

    if magic in 'PACK':
        extract_archive(out, name, f, parent_invrec)
    elif magic in ('PK\x03\x04',):
        extract_zip(out, name, f, parent_invrec)
    elif magic in raw_types:
        name += '.' + raw_types[magic]
        dump_file(out, name, f, parent_invrec)
    else:
        print "Unknown magic", repr(magic)
        assert False

def extract_archive(out, name, f, parent_invrec, check_magic='PACK'):
    magic = f.read(4)
    assert magic == check_magic

    invrec = Invrec(name, magic)
    parent_invrec.children.append(invrec)

    n_files = lw(f)
    toc = []

    for i in xrange(n_files):
        name = 'file_%04d' % (i, )
        offs = lw(f)
        size = lw(f)
        toc.append((name, offs, size))

    for ent in toc:
        name, offs, size = ent

        f.seek(offs, os.SEEK_SET)
        child_f = StringIO(f.read(size))
        extract_data(out, name, child_f, invrec)

def extract_zip(out, name, f, parent_invrec):
    invrec = Invrec(name, 'zip')
    parent_invrec.children.append(invrec)

    z = zipfile.ZipFile(f)
    names = z.namelist()
    assert len(names) == 1
    name = names[0]

    child_f = z.open(name, 'r')
    dump_file(out, name, child_f, invrec)

def dump_file(out, name, f, parent_invrec):
    invrec = Invrec(name, 'data')
    parent_invrec.children.append(invrec)

    out.dump(name, f)

extract_toplevel(sys.argv[1])
