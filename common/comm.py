class Message(object):
    def __init__(self,status=500,body="Something wrong...",port=0,libs=None):
        self.status = status
        self.body = body
        self.port = port
        self.libs = libs
    def jsonify(self):
        return {k: v for k, v in self.__dict__.items() if v != None}