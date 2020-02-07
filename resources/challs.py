import os
import werkzeug
import json
from pathlib import Path
from flask import jsonify, Response, send_from_directory
from flask_restful import Resource, reqparse, abort
from papaWhale import context
from papaWhale.challs import list_challs, run_chall
from papaWhale.challs import restart_challs
from papaWhale.challs import terminate_challs
from common.comm import Message

SUCCESS = 200

class ChallengeListAPI(Resource):
    def get(self):
        return list_challs()

class ChallengeUploadAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("props", required=True, type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument("file", required=True, type=werkzeug.datastructures.FileStorage, location='files')

        args = parser.parse_args()
        resp = run_chall(args)

        if resp.status == SUCCESS:
            return resp.jsonify()
        else:
            return Response(response = json.dumps(resp.jsonify()),status = resp.status,mimetype='application/json')
        
class ChallengeRestartAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        props = parser.parse_args()
        name = props["name"]
        msg = restart_challs(name)

        if msg.status==SUCCESS:
            return msg.jsonify()
        else:
            return Response(response=json.dumps(msg.jsonify()),status=msg.status,mimetype='application/json')

class ChallengeTerminateAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        props = parser.parse_args()
        name = props["name"]
        msg = terminate_challs(name)

        if msg.status==SUCCESS:
            return msg.jsonify()
        else:
            return Response(response=json.dumps(msg.jsonify()),status=msg.status,mimetype='application/json')

class ChallengeDownloadAPI(Resource):
    def get(self, chall_name):
        dist_path = Path("dock_{}".format(chall_name)).joinpath("dist.tar.gz")
        
        return send_from_directory(
            context.supplier, 
            str(dist_path), 
            as_attachment=True, 
            attachment_filename="dist.tar.gz"
        )