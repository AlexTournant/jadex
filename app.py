from flask import Flask, render_template, redirect
import requests
from unidecode import unidecode

from bdPokedex import init_db
from forms.LoginForm import LoginForm
from forms.PokemonForm import PokemonForm
from forms.RegisterForm import RegisterForm
from requeteBD import *
from insertionBD import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète'
app.secret_key = 'Ma clé secrète'

# USER
est_connecte = False
nom = None
id = None

# DB
init_db()


@app.route('/', methods=['GET', 'POST'])
def streetform():
    global est_connecte
    form = PokemonForm()
    pokemon_names = load_pokemon_names()
    if form.validate_on_submit():
        pokemon_name = form.pokemon.data
        pokemon_id = get_pokemon_id_by_name(pokemon_name)
        if pokemon_id != -1:
            print(pokemon_id)
            r = requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + str(pokemon_id))
            pokemon_info = r.json()
            inCollection = False
            if est_connecte:
                inCollection = isInCollection(pokemon_id, id)
            return render_template('show.html', info=pokemon_info, form=form, pokemon_names=pokemon_names, nom=nom,
                                   est_connecte=est_connecte, inCollection=inCollection, id_pokemon=pokemon_id)
    return render_template('form.html', form=form, pokemon_names=pokemon_names, nom=nom, est_connecte=est_connecte)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    global est_connecte, id, nom
    form = PokemonForm()
    pokemon_names = load_pokemon_names()
    if form.validate_on_submit():
        pokemon_name = form.pokemon.data
        pokemon_id = get_pokemon_id_by_name(pokemon_name)
        if pokemon_id != -1:
            print(pokemon_id)
            r = requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + str(pokemon_id))
            pokemon_info = r.json()
            inCollection = False
            if est_connecte:
                inCollection = isInCollection(pokemon_id, id)
            return render_template('show.html', info=pokemon_info, form=form, pokemon_names=pokemon_names, nom=nom,
                                   est_connecte=est_connecte, inCollection=inCollection, id_pokemon=pokemon_id)
    formulaire = LoginForm()
    if formulaire.validate_on_submit():
        if IsInBD(formulaire.nom.data, formulaire.mdp.data):
            nom = formulaire.nom.data
            est_connecte = True
            id = ID_selon_mdp_et_nom(formulaire.nom.data, formulaire.mdp.data)
            return redirect('/')
    message = "c'est pas bon"
    return (
        render_template('login.html', pokemon_names=pokemon_names, formulaire=formulaire, form=form, message=message,
                        nom=nom, est_connecte=est_connecte))


@app.route('/register', methods=['GET', 'POST'])
def register():
    global est_connecte, nom, id
    form = PokemonForm()
    pokemon_names = load_pokemon_names()
    if form.validate_on_submit():
        pokemon_name = form.pokemon.data
        pokemon_id = get_pokemon_id_by_name(pokemon_name)
        if pokemon_id != -1:
            print(pokemon_id)
            r = requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + str(pokemon_id))
            pokemon_info = r.json()
            inCollection = False
            if est_connecte:
                inCollection = isInCollection(pokemon_id, id)
            return render_template('show.html', info=pokemon_info, form=form, pokemon_names=pokemon_names, nom=nom,
                                   est_connecte=est_connecte, inCollection=inCollection, id_pokemon=pokemon_id)
    formulaire = RegisterForm()
    if formulaire.validate_on_submit():
        print((formulaire.nom.data, formulaire.mdp.data))
        insertionTableAuthentification((formulaire.nom.data, formulaire.mdp.data))
        nom = formulaire.nom.data
        est_connecte = True
        id = ID_selon_mdp_et_nom(formulaire.nom.data, formulaire.mdp.data)
        return redirect('/')
    return render_template('register.html', pokemon_names=pokemon_names, formulaire=formulaire, form=form,
                           est_connecte=est_connecte, nom=nom)


@app.route('/logout')
def logout():
    global est_connecte, nom
    est_connecte = False
    nom = None
    return redirect('/')


@app.route('/collection', methods=['GET'])
def collection():
    form = PokemonForm()
    pokemon_names = load_pokemon_names()
    if form.validate_on_submit():
        pokemon_name = form.pokemon.data
        pokemon_id = get_pokemon_id_by_name(pokemon_name)
        if pokemon_id != -1:
            print(pokemon_id)
            r = requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + str(pokemon_id))
            pokemon_info = r.json()
            inCollection = False
            if est_connecte:
                inCollection = isInCollection(pokemon_id, id)
            return render_template('show.html', info=pokemon_info, form=form, pokemon_names=pokemon_names, nom=nom,
                                   est_connecte=est_connecte, inCollection=inCollection, id_pokemon=pokemon_id)
    tab = []
    for pokemon_id in CollectionAll(id):
        r = requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/" + str(pokemon_id))
        tab.append({"id": pokemon_id, "pokemon": r.json()})
    return (render_template('collection.html', form=form, collection=tab, pokemon_names=pokemon_names, nom=nom,
                            est_connecte=est_connecte))


@app.route('/ajoutCollection/<id_pokemon>', methods=['GET'])
def ajoutCollection(id_pokemon):
    message = "Probleme lors de l'ajout"
    if est_connecte:
        print(id, type(id), id_pokemon, type(id_pokemon))
        if insertionTableCollection((id_pokemon, id)):
            message = "Bien ajouter"
    print(message)
    return redirect('/')


@app.route('/suppCollection/<id_pokemon>', methods=['GET'])
def suppCollection(id_pokemon):
    message = "Probleme lors de la suppression"
    if est_connecte:
        if suppPokemon(id_pokemon, id):
            message = "Bien supprimer"
    print(message)
    return redirect('/')


if __name__ == '__main__':
    app.run()
