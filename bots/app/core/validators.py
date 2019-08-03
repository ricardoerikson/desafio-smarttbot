from wtforms.validators import ValidationError

def positive_value(form, field):
	if field.data <= 0:
		raise ValidationError('Valor deve ser maior que 0.')
