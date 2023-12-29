import base64
import sqlite3
from sqlite3 import Error

from adodbapi import Error

def IsInBD(nom:str,mdp:str):
    sample_string = mdp
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    print(base64_string)
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        select id 
        from Authentification 
        where nom=? and mdp=?;
        """,(nom,base64_string))
        res=cur.fetchall()
        if len(res)==1:
            return True
        return False
    except Error:
        print("erreur sql")
    except IndexError:
        print("il n'y a pas cette ligne dans la table")
    finally:
        cur.close()
        conn.close()


def ID_selon_mdp_et_nom(nom:str,mdp:str)->int:
    """
    recuperer l'id selon le mdp et le nom de l'utilisateur donnee en parametre
    :param nom:
    :param mdp:
    :return int:
    """
    try:
        sample_string=mdp
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        newMdp = base64_bytes.decode("ascii")
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        select id 
        from Authentification 
        where nom=? and mdp=?;
        """,(nom,newMdp))
        res=cur.fetchall()
        return res[0][0]
    except Error:
        print("erreur sql")
    except IndexError:
        print("il n'y a pas cette ligne dans la table")
    finally:
        cur.close()
        conn.close()

def suppPokemon(id_pokemon:int,id_user:int)->bool:
    """
    supprime le pokemon d'id donnee en parametre
    :param id:
    :return bool:
    """
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        delete from Collection where id=? and id_p=?;
        """,(id_pokemon,id_user,))
        conn.commit()
        return cur.rowcount > 0
    except Error:
        print("erreur")
    finally:
        cur.close()
        conn.close()

def majMdp(name:str,mdp:str,newMdp:str)->bool:
    """
    met a jour le mot de passe de l'utilisateur si il veut le changer
    :param name:
    :param mdp:
    :param newMdp:
    :return bool:
    """
    id = ID_selon_mdp_et_nom(name, mdp)
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        update Authentification
        set mdp=?
        where id=?;
        """,(newMdp,id))
        conn.commit()
        return cur.rowcount > 0
    except Error:
        print("erreur")
    finally:
        cur.close()
        conn.close()

def majNom(name:str,newNom:str,mdp:str)->bool:
    """
    met a jour le nom de l'utilisateur si il veut le changer
    :param name:
    :param newNom:
    :param mdp:
    :return bool:
    """
    id=ID_selon_mdp_et_nom(name,mdp)
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        update Authentification
        set nom = ?
        where id = ?;
        """,(newNom,id))
        conn.commit()
        return cur.rowcount>0
    except Error:
        print("erreur")
    finally:
        cur.close()
        conn.close()

def CollectionAll(id:int)->list:
    tab=[]
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        select * 
        from Collection
        where id_p=?
        """,(id,))
        conn.commit()
        res = cur.fetchall()
        for i in res:
            tab.append(i[0])
        return tab
    except Error:
        print("il ne trouve pas l'id donnee en parametre ")
    finally:
        cur.close()
        conn.close()

def isInCollection(id_pokemon:int,id_user:int):
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        select * 
        from Collection
        where id=? and id_p=?
        """,(id_pokemon,id_user,))
        conn.commit()
        res = cur.fetchall()
        print(res)
        if len(res)==1:
            return True
        return False
    except Error:
        print("il ne trouve pas l'id donnee en parametre ")
    finally:
        cur.close()
        conn.close()