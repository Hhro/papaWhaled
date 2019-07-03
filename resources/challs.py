from flask import jsonify
from flask_restful import Resource, reqparse, abort
from papaWhale.challs import list_challs
from papaWhale.challs import restart_challs

SUCCESS=200
NOT_EXIST=404
SERVER_ERROR=500

class ChallengeListAPI(Resource):
    def get(self):
        return list_challs()

class ChallengeUploadAPI(Resource):
    def post(self):
        pass

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