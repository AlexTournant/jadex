import sqlite3
from sqlite3 import IntegrityError
import hashlib
def insertionTableCollection(liste:tuple):
    insert = True
    if not len(liste) == 2:
        insert = False
    if insert:
        """
        insertion des valeur dans la collection tout en faisant attention a l'injection
        """
        try:
            conn = sqlite3.connect("Pokedex.db")
            conn.execute('PRAGMA foreign_keys = ON')
            cur = conn.cursor()
            cur.execute("insert into Collection(id,date, id_P) values(?, DATE('now'),?)",liste)
            conn.commit()
        except IntegrityError :
            conn.rollback()
            print("le pokemon est deja dans la collection")
        finally:
            cur.close()
            conn.close()

def insertionTableAuthentification(liste:tuple):
    insert=True
    if not len(liste)==2:
        insert=False
    if insert:
        """
        insertion des valeur dans l'authentification tout en faisant attention a l'injection
        """
        try:
            conn = sqlite3.connect("Pokedex.db")
            cur = conn.cursor()
            cur.execute("insert into Authentification(nom, mdp) values (?,?)",liste)
            conn.commit()
        except IntegrityError:
            print("le nom a deja ete pris ")
        finally:
            cur.close()
            conn.close()

insertionTableAuthentification(('alex','alex2004'))
insertionTableCollection((1,1))
