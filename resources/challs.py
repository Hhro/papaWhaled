from flask import jsonify
from flask_restful import Resource, reqparse, abort
from papaWhale.challs import list_challs
from papaWhale.challs import restart_challs
from papaWhale.challs import run_auto_chall, run_cdock_chall, run_custom_chall
from papaWhale.dockutils import find_avail_port, check_port_avail
import werkzeug

SUCCESS=200
NOT_EXIST=404
SERVER_ERROR=500

class ChallengeListAPI(Resource):
    def get(self):
        return list_challs()

class ChallengeUploadAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name",required=True,type=str)
        parser.add_argument("arch",type=str)
        parser.add_argument("chal-type",required=True,type=str)
        parser.add_argument("ver",type=str)
        parser.add_argument("port",type=str)
        parser.add_argument("docker-file",type=str)
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
            check_port_avail(port)
        
        if chal_type == "auto":
            arch = args["arch"]
            ver = args["ver"]
        elif chal_type == "custom_dock":
            docker_file = args["docker-file"]
        elif chal_type == "full_custom":
            run_sh = args["run-sh"]
            stop_sh = args["stop-sh"]

        chal_file = args["file"]

        if chal_type == "auto":
            status = run_auto_chall(name,port,arch,ver,chal_file,flag)
        elif chal_type == "custom_dock":
            status = run_cdock_chall(name,port,docker_file,chal_file)
        elif chal_type == "full_custom":
            status = run_custom_chall(name,port,run_sh,stop_sh,chal_file)
        
        if status == SUCCESS:
            msg = "Running {} succeeded.".format(name)
        elif status == SERVER_ERROR:
            msg = "Error occuered. Check again please"

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