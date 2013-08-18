from shared import db
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20))
	def __init__(self,name):
		self.name = name