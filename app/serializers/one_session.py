class OneSession:
    def serialize(self, data):
        return dict(session=data.to_dict())
