from flask import Flask, render_template, redirect
import requests
from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'

class PokemonForm(FlaskForm):
    pokemon = StringField('Pokemon', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def streetform():

    form = PokemonForm()
    if form.validate_on_submit():
        pokemon = form.pokemon.data
        print(pokemon)
        r = requests.get("https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + pokemon)
        pokemon_info = r.json()

        return render_template('show.html', info=pokemon_info, form=form)

    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run()
