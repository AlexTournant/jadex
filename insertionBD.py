import base64
import sqlite3
from sqlite3 import IntegrityError

from numpy.core.defchararray import lower

sample_string = "GeeksForGeeks is the best"
sample_string_bytes = sample_string.encode("ascii")

base64_bytes = base64.b64encode(sample_string_bytes)
base64_string = base64_bytes.decode("ascii")

print(base64_string)
base64_string = " R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA =="
base64_bytes = base64_string.encode("ascii")

sample_string_bytes = base64.b64decode(base64_bytes)
sample_string = sample_string_bytes.decode("ascii")
print(sample_string)

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
    if len(liste)==2:
        sample_string = liste[1]
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        newMdp = base64_bytes.decode("ascii")
        new_tuple =(liste[0],newMdp)

    if insert:
        """
        insertion des valeur dans l'authentification tout en faisant attention a l'injection
        """
        try:
            conn = sqlite3.connect("Pokedex.db")
            cur = conn.cursor()
            cur.execute("insert into Authentification(nom, mdp) values (?,?)",new_tuple)
            conn.commit()
            return True
        except IntegrityError as e:
            if lower(e.args[0].split()[0])== "check":
                if str(e.args[0].split(":")[1].split(">")[0]).strip() == "nom":
                     print("le nom n'est pas assez grand ")
                elif str(e.args[0].split(":")[1].split(">")[0]).strip() == "mdp":
                    print("mdp n'est pas assez grand")
            else:
                print("le nom ou le mot de passe a deja ete pris")
            return False
        finally:
            cur.close()
            conn.close()

insertionTableCollection((1,1))