import json
from pathlib import Path
from flask import Response
from papaWhale.challs import run_auto_chall, run_cdock_chall, run_custom_chall
from papaWhale.dockutils import find_avail_port, check_port_avail
from common.comm import Message

SUCCESS = 200
NOT_EXIST = 404
COLLISION = 409
SERVER_ERROR = 500

def load_props(chall_dir):
    props_path = chall_dir.joinpath("props.json")
    if not props_path.exists():
        return False
    else:
        return json.load(open(str(props_path),"r"))

def load_props_template(tmpl_name):
    tmpl_path = tmpl_dir.joinpath(tmpl_name+".json")
    if not tmpl_path.exists():
        return False
    else:
        return json.load(open(str(props_path),"r"))

def save_props(chall_dir, props, replace=True):
    props_path = chall_dir.joinpath("props'json")

    if props_path.exists() and not replace:
        return False
    else:
        json.dump(props, open(str(props_path),"w"))

def prepare_props_from_args(chall_dir,args):
    props = load_props_template("default")
    props_keys = ["name", "arch", "chal-type", "flag", "deps"]

    props.update({key: args[key] for key in props_keys})
    save_props(chall_dir, props)

def check_props(chall_dir, props=None):
    if props == None:
        props = load_props(chall_dir)
    
    required_keys = ["name", "arch", "chal_type", "flag"]

    for key in required_keys:
        if key not in props.keys():
            return False

    return True
    
def process_props(props=None):
    msg = Message(str(SERVER_ERROR),"Something Wrong...")

    if props == None:
        props = load_props()
    name = props["name"]
    port = props["port"]
    flag = props["flag"]
    chal_type = props["chal-type"]

    if port == "auto":
        port = find_avail_port()
    else:
        if not check_port_avail(port):
            msg = Message(COLLISION,"port {} is already used.".format(port))
            return Response(response=json.dumps(msg.jsonify()),status=msg.status,mimetype='application/json')
    
    if chal_type == "auto":
        arch = props["arch"]
        ver = props["ver"]
    elif chal_type == "custom_dock":
        dockerfile = props["dockerfile"]
    elif chal_type == "full_custom":
        run_sh = props["run-sh"]
        stop_sh = props["stop-sh"]

    chal_file = props["file"]

    if chal_type == "auto":
        msg = run_auto_chall(name,port,arch,ver,chal_file,flag)
    elif chal_type == "custom_dock":
        msg = run_cdock_chall(name,port,chal_file,dockerfile,flag)
    elif chal_type == "full_custom":
        msg = run_custom_chall(name,port,run_sh,stop_sh,chal_file,flag)
    
    if msg.status == SUCCESS:
        return msg.jsonify()
    else:
        return Response(response=json.dumps(msg.jsonify()),status=msg.status,mimetype='application/json')
