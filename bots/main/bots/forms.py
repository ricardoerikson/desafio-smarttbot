from flask_wtf import FlaskForm
from wtforms import (validators, DecimalField, StringField, BooleanField, HiddenField, SelectField,
					SubmitField, IntegerField)
from wtforms.validators import DataRequired, ValidationError
from main.core.validators import positive_value

import re

tooltip = {'data-toggle': 'tooltip', 'data-placement': 'bottom'}

class BotsForm(FlaskForm):

	id        = HiddenField()
	name      = StringField('Nome: ', validators=[DataRequired(message='Campo obrigatório')])
	amount    = DecimalField('Quantidade a ser negociada', places=8, validators=[DataRequired(message='Campo obrigatório com valor fracionado. ex: 0.0001'), positive_value])
	period    = StringField('Período', validators=[DataRequired(message='Campo obrigatório')], \
				render_kw={**tooltip, **{'placeholder': 'Ex: 5m, 1h, 1d', 'title': 'Tempo gráfico dos candles. Utilize "m", "h" e "d" para minutos, hora dias, respectivamente. \
				Para tempo em minutos, o valor deve ser múltiplo de 5 minutos. Exemplos:  5m, 15m, 1h ou 1d.'}})
	gain_size = DecimalField('Gain padrão', places=8, validators=[DataRequired(message='Campo obrigatório com valor fracionado. ex: 0.003'), positive_value], \
				render_kw={**tooltip, **{'placeholder': 'Ex: 0.0003', 'title': 'Retorno pretendido pela estratégia. Em operação comprada, o preço alvo = gain padrão + preço de entrada'}})
	loss_size = DecimalField('Loss padrão', places=8, validators=[DataRequired(message='Campo obrigatório com valor fracionado. ex: 0.001'), positive_value], \
				render_kw={**tooltip, **{'placeholder': 'Ex: 0.00001', 'title': 'Risco da estratégia. Em uma operação comprada, o stop loss = preço de entrada - loss padrão'}})
	short_sma = IntegerField('Média móvel curta', validators=[DataRequired(message='Campo obrigatório com valor inteiro positivo. Ex: 9'), positive_value], \
				render_kw={**tooltip, **{'title':'Quantidade de períodos da média móvel'}})
	long_sma  = IntegerField('Média móvel longa', validators=[DataRequired(message='Campo obrigatório com valor inteiro positivo. Ex: 21'), positive_value], \
				render_kw={**tooltip, **{'title':'Quantidade de períodos da média móvel'}})
	active    = BooleanField('Ativado')
	currency_pair_id = SelectField('Par de moedas', coerce=int, validators=[ DataRequired(message = 'Campo obrigatório')])

	submit    = SubmitField('Salvar')

	def validate_period(form, field):
		regex = r"^[0-9]+[hmd]$"
		result = re.search(regex, field.data, re.MULTILINE)
		if result is None:
			raise ValidationError('Utilize o seguinte formato: 5m, 30m, 2h, 3d')

		number = int(''.join(filter(str.isdigit, field.data)))
		letter = ''.join(filter(str.isalpha, field.data))

		if (letter is 'm') and (number % 5 is not 0):
			raise ValidationError('O número deve ser múltiplo de 5 para tempo em minutos')


	def validate_long_sma(form, field):
		if field.data <= form.short_sma.data:
			raise ValidationError('A média móvel longa deve ter período maior que a curta.')
