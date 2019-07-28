import json
import subprocess

def do_chall_test(path,port,flag):
    props = {}

    with open(str(path.joinpath("props.json"))) as props_in:
        props = json.load(props_in)
    
    test_worker = props["test"]

    if subprocess.check_call([str(path.joinpath(test_worker)),port,flag],cwd=str(path)):
        return True
    else:
        return False
