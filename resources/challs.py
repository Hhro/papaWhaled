from flask import jsonify
from flask_restful import Resource, reqparse, abort
from papaWhale.challs import list_challs
from papaWhale.challs import restart_challs
from papaWhale.challs import run_auto_chall, run_cdock_chall, run_custom_chall
from papaWhale.dockutils import find_avail_port, check_port_avail
from common.comm import Message
import werkzeug

SUCCESS=200
NOT_EXIST=404
COLLISION=409
SERVER_ERROR=500

class ChallengeListAPI(Resource):
    def get(self):
        return list_challs()

class ChallengeUploadAPI(Resource):
    def post(self):
        msg = Message("500","Something Wrong...")
        parser = reqparse.RequestParser()
        parser.add_argument("name",required=True,type=str)
        parser.add_argument("arch",type=str)
        parser.add_argument("chal-type",required=True,type=str)
        parser.add_argument("ver",type=str)
        parser.add_argument("port",type=str)
        parser.add_argument("dockerfile",type=str)
        parser.add_argument("run-sh",type=str)
        parser.add_argument("stop-sh",type=str)
        parser.add_argument("file",required=True,type=werkzeug.datastructures.FileStorage,location='files')
        parser.add_argument("flag",required=True,type=str)

        args = parser.parse_args()
        name = args["name"]
        port = args["port"]
        flag = args["flag"]
        chal_type = args["chal-type"]

        if port == "auto":
            port = find_avail_port()
        else:
            if not check_port_avail(port):
                msg = Message(COLLISION,"port {} is already used.".format(port))
                return msg.jsonify()
        
        if chal_type == "auto":
            arch = args["arch"]
            ver = args["ver"]
        elif chal_type == "custom_dock":
            dockerfile = args["dockerfile"]
        elif chal_type == "full_custom":
            run_sh = args["run-sh"]
            stop_sh = args["stop-sh"]

        chal_file = args["file"]

        if chal_type == "auto":
            msg = run_auto_chall(name,port,arch,ver,chal_file,flag)
        elif chal_type == "custom_dock":
            msg = run_cdock_chall(name,port,chal_file,dockerfile,flag)
        #TODO
        elif chal_type == "full_custom":
            status = run_custom_chall(name,port,run_sh,stop_sh,chal_file)
        
        return msg.jsonify()

class ChallengeRestartAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        args = parser.parse_args()
        name = args["name"]
        status = restart_challs(name)

        if status==SUCCESS:
            msg = "Restart {} succeeded.".format(name)
            return jsonify(msg=msg)
        elif status==NOT_EXIST:
            abort(404,msg="Challenge {} is not exist.".format(name))
        elif status==SERVER_ERROR:
            abort(500,msg="Restart {} failed".format(name))