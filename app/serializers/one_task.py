class OneTask:
    def serialize(self, data):
        return dict(task=data.to_dict())

