import sqlite3
from sqlite3 import OperationalError

"""
Créé la table Collection
id = identifiant du pokemon 
date = date a laquelle le pokemon a ete rajouté a la collection
id_P = id de la personne réferencé
"""
try:
    conn = sqlite3.connect("Pokedex.db")
    cur = conn.cursor()
    cur.execute("""
    create table Collection(
    id INTEGER PRIMARY KEY ,
    date date not null,
    id_P integer not null ,
     FOREIGN KEY (id_P) REFERENCES Authentification(id)
    )
    """)
except OperationalError:
    print("La table Collection a deja été créé")
finally:
    cur.close()
    conn.close()

"""
Créé la table Authentification
id = identifiant de la personne 
nom = nom de la personne 
mdp = mot de passe de la personne 
"""
try:
    conn = sqlite3.connect("Pokedex.db")
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.cursor()
    cur.execute("""
    create table Authentification(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nom varchar(15) not null unique ,
    mdp varchar(20) not null unique ,
    check ( nom>1 ),
    check ( mdp>5 )
    )
    """)
except OperationalError:
    print("La table Authentification a deja été créé")
finally:
    cur.close()
    conn.close()