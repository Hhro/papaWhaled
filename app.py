import sys
import argparse
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sslify import SSLify
from resources.challs import ChallengeListAPI
from resources.challs import ChallengeUploadAPI
from resources.challs import ChallengeRestartAPI
from resources.challs import ChallengeTerminateAPI

app = Flask(__name__)
cors = CORS(app,resources={"/*":{"origins":"*"}})
api = Api(app)

api.add_resource(ChallengeListAPI,'/challs',endpoint="challenges")
api.add_resource(ChallengeUploadAPI,'/challs/upload',endpoint="challenge_upload")
api.add_resource(ChallengeRestartAPI,'/challs/restart',endpoint="challenge_restart")
api.add_resource(ChallengeTerminateAPI,'/challs/term',endpoint="challenge_terminate")

parser = argparse.ArgumentParser()
parser.add_argument("--ssl",action="store_true")
parser.add_argument("--pem")
parser.add_argument("--crt")
parser.add_argument("-d","--debug",action="store_true")
parser.add_argument("-p","--port")
args = parser.parse_args()

if args.ssl:
    context = (args.crt,args.pem)
    sslify = SSLify(app)

    app.run(debug=args.debug, host='0.0.0.0', port=args.port, ssl_context=context)
else:
    app.run(debug=args.debug, host='0.0.0.0', port=args.port)
