import sys, os
import argparse
from pathlib import Path
from papaWhale import context
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sslify import SSLify

app = Flask(__name__)
cors = CORS(app,resources={"/*":{"origins":"*"}})
api = Api(app)

parser = argparse.ArgumentParser()
parser.add_argument("--supplier", 
                    help = "Supplier path",
                    required=True)
parser.add_argument("--ssl", 
                    help = "Run server on SSL.",
                    action="store_true")
parser.add_argument("--pem",
                    help = "SSL pem key. Required if you run on ssl mode.")
parser.add_argument("--crt",
                    help = "SSL certificate. Required if you run on ssl mode.")
parser.add_argument("-d","--debug",
                    help = "Run flask server as debug mode",
                    action = "store_true")
parser.add_argument("-p", "--port",
                    help = "API server port",
                    default = 31337)
parser.add_argument("--backup",
                    help = "On error, back up the challenge directory as name.bak",
                    action = "store_true",
                    default = False)
args = parser.parse_args()

context.supplier = Path(args.supplier).absolute()
context.backup = args.backup

from resources.challs import ChallengeListAPI
from resources.challs import ChallengeUploadAPI
from resources.challs import ChallengeRestartAPI
from resources.challs import ChallengeTerminateAPI
from resources.challs import ChallengeDownloadAPI

api.add_resource(ChallengeListAPI,'/challs',endpoint="challenges")
api.add_resource(ChallengeUploadAPI,'/challs/upload',endpoint="challenge_upload")
api.add_resource(ChallengeRestartAPI,'/challs/restart',endpoint="challenge_restart")
api.add_resource(ChallengeTerminateAPI,'/challs/term',endpoint="challenge_terminate")
api.add_resource(ChallengeDownloadAPI,'/challs/download/<string:chall_name>',endpoint="challenge_download")

if args.ssl:
    ctx = (args.crt,args.pem)
    sslify = SSLify(app)

    app.run(debug=args.debug, host='0.0.0.0', port=args.port, ssl_context=ctx)
else:
    app.run(debug=args.debug, host='0.0.0.0', port=args.port)
