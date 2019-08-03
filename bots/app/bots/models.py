from app import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

class Bot(db.Model):
	__tablename__ = 'bots'

	id             = db.Column(db.Integer, primary_key=True)
	name           = db.Column(db.String(50), nullable=False)
	amount         = db.Column(db.Float, nullable=False)
	loss_size      = db.Column(db.Float, nullable=False)
	gain_size      = db.Column(db.Float, nullable=False)
	period         = db.Column(db.String(10), nullable=False)
	short_sma      = db.Column(db.Integer, nullable=False)
	long_sma       = db.Column(db.Integer, nullable=False)
	active         = db.Column(db.Boolean, default=False)

	__created      = db.Column(db.DateTime, default=datetime.now)
	__last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

	trades         = db.relationship('Trade', backref='bot', uselist=True, lazy='dynamic')
	currency_pair  = db.relationship('CurrencyPair', uselist=False)
	currency_pair_id  = db.Column(db.Integer, db.ForeignKey('currency_pairs.id'))

	@hybrid_property
	def created(self):
		return self.__created

	@hybrid_property
	def last_updated(self):
		return self.__last_updated

	@hybrid_method
	def position(self):
		return  self.trades.filter_by(exit_price=None).first()

	def __repr__(self):
		return f"#{self.id} Bot name is: {self.name}. short sma: {self.short_sma} and long sma: {self.long_sma}"

class Trade(db.Model):
	__tablename__ = 'trades'

	id               = db.Column(db.Integer, primary_key=True)
	open_time        = db.Column(db.DateTime, nullable=False, default=datetime.now)
	close_time       = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
	enter_price      = db.Column(db.Float(precision='16,8'), nullable=False)
	exit_price       = db.Column(db.Float(precision='16,8'), nullable=True)
	amount           = db.Column(db.Float(precision='16,8'), nullable=False)
	trade_type       = db.Column(db.String(1), nullable=False)

	currency_pair    = db.relationship('CurrencyPair', uselist=False)
	currency_pair_id = db.Column(db.Integer, db.ForeignKey('currency_pairs.id'), nullable=False)
	bot_id           = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)



	def __repr__(self):
		return f"Trade #{self.id}, currency_pair: {self.currency_pair.code}, trade_type: {self.trade_type}, enter_price: {self.enter_price}, exit_price: {self.exit_price}"

	@hybrid_property
	def buy_price(self):
		if self.trade_type == 'B':
			return self.enter_price
		if self.is_open:
			return None
		return self.exit_price

	@hybrid_property
	def sell_price(self):
		if self.trade_type == 'S':
			return self.enter_price
		if self.is_open:
			return None
		return self.exit_price

	@hybrid_method
	def result(self, current_price):
		if self.is_open:
			if self.trade_type == 'B':
				return (current_price - self.buy_price) * self.amount
			else:
				return (self.sell_price - current_price) * self.amount
		return (self.sell_price - self.buy_price) * self.amount

	@hybrid_property
	def is_open(self):
		return self.exit_price is None

