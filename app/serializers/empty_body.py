from flask import Response

class EmptyBody:
    def serialize(self, data):
        return Response(mimetype="application/json")

