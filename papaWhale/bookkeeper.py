import json
import shutil
from pathlib import Path
from papaWhale.common import get_hash
from papaWhale.context import repo

HIT = True
MISS = False

lookup = lambda hint: json.load(open(str(repo.joinpath("map.json")),"r"))[hint]

def caching_libs(chall_dir_path, props):
    libs = props["libs"]
    lib_map_path = repo.joinpath("map.json")
    lib_map = json.load(open(str(lib_map_path)))
    lib_hashes = []
    cache = [str(x.stem) for x in repo.glob('*')]

    for lib in libs:
        lib_path = chall_dir_path.joinpath(lib)
        lib_hash = get_hash(str(lib_path))
        lib_hashes.append(lib_hash)

        if lib_hash not in cache:
            lib_map.update({lib_hash:lib})
            shutil.move(str(lib_path), str(repo.joinpath(lib_hash)))
        else:
            lib_path.unlink()
    
    json.dump(lib_map,open(str(lib_map_path),"w"))
    return lib_hashes