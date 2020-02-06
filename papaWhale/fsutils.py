import shutil
import pathlib
import tarfile
import zipfile
import json
from papaWhale.props import load_props

is_dir_exist = lambda p : p.exists() and p.is_dir()
backup = lambda p : p.replace(str(p)+".bak")
cleanup = lambda p : shutil.rmtree(str(p))

def init_chall_dir(path,chall_file,flag):
    path.mkdir()
    chall_path = str(path.joinpath("chall.zip"))
    flag_path = str(path.joinpath("flag"))
    chall_file.save(chall_path)

    #unzip chall.zip file
    with zipfile.ZipFile(chall_path, 'r') as zip_in:
        zip_in.extractall(str(path))
    
    with open(flag_path,'w') as flag_out:
        flag_out.write(flag)
        flag_out.close()

def make_dist(chall_dir, props):
    dist = tarfile.open(
        str(chall_dir.joinpath("dist.tar.gz")),
        "w:gz"
    )
    
    for distee in props["dist"]:
        dist.add(chall_dir.joinpath(props[distee]))
    dist.close()
    
def check_chall_dir(chall_dir, props):
    req_props = []
    props = load_props(chall_dir)
    chall_type = props["chal-type"]

    if not chall_dir.joinpath("props.json").exists():
        return False
    
    if chall_type == "auto":
        req_props = ["bin","test"]
    elif chall_type == "cdock":
        req_props = ["bin","test"]
    elif chall_type == "custom":
        req_props = ["init.sh","run.sh"]
    
    for prop in req_props:
        if prop not in props.keys() or props[prop] == '':
            return False
        else:
            if not chall_dir.joinpath(props[prop]).exists():
                return False
    if not chall_dir.joinpath("dist.tar.gz").exists():
        return False

    chall_dir.joinpath("chall.zip").unlink()
    return True

def set_chall_dir_perm(chall_path, props):
    perms = props["perms"]

    #Set file permission
    for perm in list(perms.keys()):
        for setee in perms[perm]:
            setee_path = chall_path.joinpath(props[setee])
            setee_path.chmod(int(perm,8))