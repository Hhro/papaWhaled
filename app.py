import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="31337")