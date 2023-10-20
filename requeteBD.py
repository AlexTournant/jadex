import sqlite3
from sqlite3 import Error

from adodbapi import Error


def ID_selon_mdp_et_nom(nom:str,mdp:str)->int:
    """
    recuperer l'id selon le mdp et le nom de l'utilisateur donnee en parametre
    :param nom:
    :param mdp:
    :return int:
    """
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        select id 
        from Authentification 
        where nom=? and mdp=?;
        """,(nom,mdp))
        res=cur.fetchall()
        return res[0][0]
    except Error:
        print("erreur sql")
    except IndexError:
        print("il n'y a pas cette ligne dans la table")
    finally:
        cur.close()
        conn.close()

def suppPokemon(id:int)->bool:
    """
    supprime le pokemon d'id donnee en parametre
    :param id:
    :return bool:
    """
    try:
        conn = sqlite3.connect("Pokedex.db")
        cur = conn.cursor()
        cur.execute("""
        delete from Collection where id=?;
        """,(id,))
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
        ID_selon_mdp_et_nom("Alex","3456787654")
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

print(CollectionAll(1))
