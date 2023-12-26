from flask import Flask, render_template, request, jsonify
import requests
from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired
from unidecode import unidecode

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'


class PokemonForm(FlaskForm):
    pokemon = StringField('Pokemon', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def streetform():
    form = PokemonForm()

    pokemon_names = load_pokemon_names()

    if form.validate_on_submit():

        pokemon_name = form.pokemon.data
        pokemon_id = get_pokemon_id_by_name(pokemon_name)

        if pokemon_id != -1:
            print(pokemon_id)
            r = requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + str(pokemon_id))
            pokemon_info = r.json()
            return render_template('show.html', info=pokemon_info, form=form, pokemon_names=pokemon_names)

    return render_template('form.html', form=form, pokemon_names=pokemon_names)


@app.route('/getFileName/<id>')
def getFileName(id):
    print(id)
    r = requests.get("https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + id)
    pokemon_info = r.json()
    son = "static/gen" + str(pokemon_info['generation']) + "/" + id + " - " + unidecode(
        pokemon_info['name']['fr'].lower()) + ".ogg"
    print(son)
    return son

def load_pokemon_names():
    r = requests.get("https://api-pokemon-fr.vercel.app/api/v1/pokemon")
    if r.status_code == 200:
        pokemon_data = r.json()

        names = [pkm['name']['fr'] for pkm in pokemon_data]
    return names

def get_pokemon_id_by_name(name):
    r = requests.get("https://api-pokemon-fr.vercel.app/api/v1/pokemon")
    if r.status_code == 200:
        pokemon_data = r.json()
        for pkm in pokemon_data:
            if (pkm['name']['fr']) == (name):
                return pkm.get('pokedexId')
    return -1

if __name__ == '__main__':
    app.run()
