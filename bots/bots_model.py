from core.model import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class Bot(db.Model):
	__tablename__ = 'bots'

	id             = db.Column(db.Integer, primary_key=True)
	name           = db.Column(db.String(50), nullable=False)
	amount         = db.Column(db.Float, nullable=False)
	loss_size      = db.Column(db.Float, nullable=False)
	gain_size      = db.Column(db.Float, nullable=False)
	short_sma      = db.Column(db.Integer, nullable=False)
	long_sma       = db.Column(db.Integer, nullable=False)
	active         = db.Column(db.Boolean, default=False)

	__created      = db.Column(db.DateTime, default=datetime.now)
	__last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

	trades         = db.relationship('Trade', backref='bot', uselist=True, lazy='select')
	currency_pair  = db.relationship('CurrencyPair', uselist=False)
	currency_pair_id  = db.Column(db.Integer, db.ForeignKey('currency_pairs.id'))

	@hybrid_property
	def created(self):
		return self.__created

	@hybrid_property
	def last_updated(self):
		return self.__last_updated

	def __repr__(self):
		return f"#{self.id} Bot name is: {self.name}. short sma: {self.short_sma} and long sma: {self.long_sma}"
