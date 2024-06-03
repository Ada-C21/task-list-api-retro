from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")


    def is_complete(self):
        return self.completed_at is not None

    def to_dict(self):
        data = dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete(),
        )

        if self.goal_id:
            data["goal_id"] = self.goal_id

        return data
    
    @classmethod
    def from_dict(cls, data):
        return Task(
            title=data["title"],
            description=data["description"],
        )