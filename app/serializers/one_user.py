class OneUser:
    def serialize(self, data):
        return dict(user=data.to_dict())
