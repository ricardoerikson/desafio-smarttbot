from core.model import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class Trade(db.Model):
	__tablename__ = 'trades'

	id               = db.Column(db.Integer, primary_key=True)
	open_time        = db.Column(db.DateTime, nullable=False, default=datetime.now)
	close_time       = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
	enter_price      = db.Column(db.Float, nullable=False)
	exit_price       = db.Column(db.Float, nullable=True)
	amount           = db.Column(db.Float, nullable=False)
	trade_type       = db.Column(db.String(1), nullable=False)

	currency_pair    = db.relationship('CurrencyPair', uselist=False)
	currency_pair_id = db.Column(db.Integer, db.ForeignKey('currency_pairs.id'))
	bot_id           = db.Column(db.Integer, db.ForeignKey('bots.id'))



	def __repr__(self):
		return f"Trade #{self.id}, currency_pair: {self.currency_pair.code}, trade_type: {self.trade_type}, enter_price: {self.enter_price}, exit_price: {self.exit_price}"