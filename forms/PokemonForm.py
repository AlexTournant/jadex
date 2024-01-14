from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired


class PokemonForm(FlaskForm):
    pokemon = StringField('Pokemon', validators=[DataRequired()])