import shutil
import pathlib
import zipfile
import json

is_dir_exist = lambda p : p.exists() and p.is_dir()

def init_chall_dir(path,chal_file,flag):
    path.mkdir()
    chall_path = str(path.joinpath("chall.zip"))
    flag_path = str(path.joinpath("flag"))
    chal_file.save(chall_path)

    #unzip chall.zip file
    with zipfile.ZipFile(chall_path, 'r') as zip_in:
        zip_in.extractall(str(path))
    
    with open(flag_path,'w') as flag_out:
        flag_out.write(flag)
        flag_out.close()
    
def check_chall_dir(path,chal_type):
    req_props = []
    props = ''

    if not path.joinpath("props.json").exists():
        return False
    else:
        with open(str(path.joinpath("props.json"))) as prop_json:
            props = json.load(prop_json)
    
    if chal_type == "auto":
        req_props = ["bin","test"]
    elif chal_type == "cdock":
        pass
    elif chal_type == "custom":
        pass
    
    for prop in req_props:
        if prop not in props.keys() or props[prop] == '':
            return False
        else:
            if not path.joinpath(props[prop]).exists():
                return False

    return True

def set_chall_dir_perm(path):
    props = {}
    with open(str(path.joinpath("props.json"))) as prop_json:
        props = json.load(prop_json)
    
    bin_file = props["bin"]
    test_file = props["test"]
    elems = [bin_file,test_file,"run.sh","build.sh","term.sh"]

    #Set executable
    for elem in elems:
        tar_path = path.joinpath(elem)
        tar_path.chmod(0o755)
    