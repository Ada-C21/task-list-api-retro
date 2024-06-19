class GoalWithTasks:
    def serialize(self, data):
        goal = data
        response = goal.to_dict()
        tasks = goal.tasks
        response["tasks"] = [task.to_dict() for task in tasks]
        return response

