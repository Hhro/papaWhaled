import shutil
import pathlib
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
    
def check_chall_dir(chall_dir, props):
    req_props = []
    props = load_props()

    if not path.joinpath("props.json").exists():
        return False
    else:
        with open(str(path.joinpath("props.json"))) as prop_json:
            props = json.load(prop_json)
    
    if chal_type == "auto":
        req_props = ["bin","test"]
    elif chal_type == "cdock":
        req_props = ["bin","test"]
    elif chal_type == "custom":
        req_props = ["init.sh","run.sh"]
    
    for prop in req_props:
        if prop not in props.keys() or props[prop] == '':
            return False
        else:
            if not path.joinpath(props[prop]).exists():
                return False
    if not path.joinpath("dist.tar.gz").exists():
        return False

    path.joinpath("chall.zip").unlink()
    return True

def set_chall_dir_perm(chall_path, props):
    elems = ["bin","test","run.sh","build.sh","term.sh"]

    #Set executable
    for elem in elems:
        tar_path = chall_path.joinpath(elem)
        tar_path.chmod(0o755)