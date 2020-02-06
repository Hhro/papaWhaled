from pathlib import Path
from papaWhale.bookkeeper import lookup
from flask import send_from_directory
from flask_restful import Resource
from papaWhale import context

class LibraryDownloadAPI(Resource):
    def get(self, hint):
        return send_from_directory(context.repo, hint, as_attachment=True, attachment_filename=lookup(hint))
