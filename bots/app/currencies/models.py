from app import db
from datetime import datetime

class CurrencyPair(db.Model):
	__tablename__ = 'currency_pairs'

	id          = db.Column(db.Integer, primary_key=True)
	exchange_id = db.Column(db.Integer, nullable=False, unique=True)
	code        = db.Column(db.String(20), nullable=False)

	def __init__(self, exchange_id, code):
		self.exchange_id = exchange_id
		self.code = code

	def __repr__(self):
		return f"#{self.id}, exchange_id:{self.exchange_id}, code: {self.code}"