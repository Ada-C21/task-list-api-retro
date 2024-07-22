class UserDto:
    def __init__(self, model):
        self.id = model.id
        self.name = model.name
        self.email = model.email

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
        )