class ShallowGoalWithTasks:
    def serialize(self, data):
        goal = data
        return dict(id=goal.id, task_ids=[task.id for task in goal.tasks])

