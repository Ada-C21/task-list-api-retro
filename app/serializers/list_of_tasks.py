class ListOfTasks:
    def serialize(self, data):
        return [task.to_dict() for task in data]

