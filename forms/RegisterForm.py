from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    mdp = StringField('mdp', validators=[DataRequired()])