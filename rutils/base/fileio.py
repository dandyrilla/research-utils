import os
import json
import pickle
import hashlib
import msgpack

import pandas as pd


def make_parent_dir(path):
    parent_dir = os.path.dirname(os.path.normpath(path))
    os.makedirs(parent_dir, exist_ok=True)


def write(out, filename):
    """Write text into file."""
    make_parent_dir(filename)
    with open(filename, 'w') as f:
        f.write(out)


def json_load(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def json_dump(data, filename, **kw):
    make_parent_dir(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, **kw)


def read_tsv(filename, **kw):
    _kw = dict(sep='\t', header=0)
    _kw.update(kw)
    df = pd.read_csv(filename, **_kw)
    return df


def to_tsv(df, filename, **kw):
    make_parent_dir(filename)
    _kw = dict(sep='\t', index=False)
    _kw.update(kw)
    df.to_csv(filename, **_kw)


def pickle_load(filename):
    """Load pickled object"""
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


def pickle_dump(obj, filename, **kw):
    """Dump pickled object"""
    make_parent_dir(filename)
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, **kw)


def pack_msgpack(o, filename):
    make_parent_dir(filename)
    with open(filename, 'wb') as f:
        msgpack.pack(o, f)


def unpack_msgpack(filename):
    with open(filename, 'rb') as f:
        return msgpack.unpack(f)


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
