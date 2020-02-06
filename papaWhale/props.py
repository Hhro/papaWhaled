import json
from pathlib import Path
from flask import Response
from papaWhale.dockutils import find_avail_port, check_port_avail
from common.comm import Message
from papaWhale.context import tmpl_dir

SUCCESS = 200
NOT_EXIST = 404
COLLISION = 409
SERVER_ERROR = 500

avail_prop = ["name","arch","ver","chal-type","flag","test","bin","build_opts","run_opts","dock_opts","dist","libs"]
required_prop = ["name","arch","ver","chal-type","flag","test","bin","dist"]

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
        return json.load(open(str(tmpl_path),"r"))

def save_props(chall_dir, props, port, replace=True):
    props_path = chall_dir.joinpath("props.json")
    props["port"] = port

    if props_path.exists() and not replace:
        return False
    else:
        json.dump(props, open(str(props_path),"w"))

def prepare_props_from_args(chall_dir,args,port):
    props = load_props_template("default")

    for prop in avail_prop:
        if prop in args.keys():
            props.update({prop:args[prop]})

    props["port"] = port
    save_props(chall_dir, props, port)

def check_props(chall_dir, props=None):
    if props == None:
        props = load_props(chall_dir)
    
    for key in required_prop:
        if key not in props.keys():
            return False

    return True