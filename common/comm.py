class Message(object):
    def __init__(self,status=500,body="Something wrong...",port=0):
        self.status = status
        self.body = body
        self.port = port
    def jsonify(self):
        return self.__dict__