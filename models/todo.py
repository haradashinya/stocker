from shared import app,db
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(40))

    def __init__(self,task):
        self.task = task
