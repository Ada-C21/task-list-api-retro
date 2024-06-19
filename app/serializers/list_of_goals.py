class ListOfGoals:
    def serialize(self, data):
        return [goal.to_dict() for goal in data]

