from flask_wtf import FlaskForm
from wtforms import (validators, FloatField, StringField, BooleanField, HiddenField, SelectField,
					SubmitField, IntegerField)
from wtforms.validators import DataRequired, ValidationError
from core.validators import positive_value

tooltip = {'data-toggle': 'tooltip', 'data-placement': 'bottom'}

class BotsForm(FlaskForm):

	id        = HiddenField()
	name      = StringField('Nome: ', validators=[DataRequired(message='Campo obrigatório')])
	amount    = FloatField('Quantidade a ser negociada', validators=[DataRequired(message='Campo obrigatório com valor fracionado. ex: 0.0001'), positive_value])
	gain_size = FloatField('Gain padrão', validators=[DataRequired(message='Campo obrigatório com valor fracionado. ex: 0.003'), positive_value], \
				render_kw={**tooltip, **{'title': 'Retorno pretendido pela estratégia. Em operação comprada, o preço alvo = gain padrão + preço de entrada'}})
	loss_size = FloatField('Loss padrão', validators=[DataRequired(message='Campo obrigatório com valor fracionado. ex: 0.001'), positive_value], \
				render_kw={**tooltip, **{'title': 'Risco da estratégia. Em uma operação comprada, o stop loss = preço de entrada - loss padrão'}})
	short_sma = IntegerField('Média móvel curta', validators=[DataRequired(message='Campo obrigatório com valor inteiro positivo. Ex: 9'), positive_value], \
				render_kw={**tooltip, **{'title':'Quantidade de períodos da média móvel'}})
	long_sma  = IntegerField('Média móvel longa', validators=[DataRequired(message='Campo obrigatório com valor inteiro positivo. Ex: 21'), positive_value], \
				render_kw={**tooltip, **{'title':'Quantidade de períodos da média móvel'}})
	active    = BooleanField('Ativado')
	currency_pair_id = SelectField('Par de moedas', coerce=int, validators=[ DataRequired(message = 'Campo obrigatório')])

	submit    = SubmitField('Salvar')

	def validate_long_sma(form, field):
		if field.data <= form.short_sma.data:
			raise ValidationError('A média móvel longa deve ter período maior que a curta.')
