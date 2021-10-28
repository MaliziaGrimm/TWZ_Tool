from flask import Flask
from flask import request
import os, time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, MetaData, Table, DATE
from sqlalchemy.sql import select 

import datenbank_obj

def spieler():
# spielerneuanlage 

# anlage Datenbank - falls nicht vorhanden
    engine = create_engine('sqlite:///daten/spieler.db')
    metadata = datenbank_obj.getdbmetadata(engine)
    spieler = datenbank_obj.spieler_dbobj(metadata)
    wertzahl = datenbank_obj.wertzahl_dbobj(metadata)
    paarung = datenbank_obj.paarung_dbbj(metadata)
    aktuelle_runde = datenbank_obj.aktuellerunde_dbobj(metadata)
    
    metadata.create_all()

#Datensatz eintragen - wenn erfasst / Fehler werden im Frontend abgefangen    
    if request.method == 'POST':
        insert_spieler = spieler.insert().values(name=request.form['form_name'], vorname=request.form['form_vorname'], aktiv="J", spielernummer=request.form['form_spielernummer'],
        datumab=request.form['form_eintrittsdatum'], ak=request.form['form_ak'], verein=request.form['form_verein'], email=request.form['form_email'], mobil=request.form['form_mobil'],
        geburtsdatum=request.form['form_geburtsdatum'], uwgprivat=request.form['form_uwgprivat'], letztergegner="0", vorletztergegner="0",
        drittletztergegner="0", partienmitw="0", partienmits="0", patienspielfrei="0")
        engine.execute(insert_spieler)
        insert_wertzahl = wertzahl.insert().values(spielernummer=request.form['form_spielernummer'], wertzahl=request.form['form_twz'])
        engine.execute(insert_wertzahl)
        insert_paarung = paarung.insert().values(spielernummer=request.form['form_spielernummer'], twz_gegner="99", brett="99", ergebnis = "99")
        engine.execute(insert_paarung)
        insert_aktuelle_runde = aktuelle_runde.insert().values(spielernummer=request.form['form_spielernummer'], aktuelles_brett="0", aktueller_gegner="0",
        aktuelle_farbe="0", aktuell_aktiv="J", aktuelle_runde="0", letztes_brett="0", letzter_gegner="0", letzte_farbe="0", letzterunde_aktiv="N", letzte_runde="0")
        engine.execute(insert_aktuelle_runde)
        pass
    else:
        pass
    return 
#ok 23092021

def spieleraktivieren():
# ist nur spieleraktivieren - deaktivieren
# anlage Datenbank - falls nicht vorhanden
    engine = create_engine('sqlite:///daten/spieler.db')

    metadata = datenbank_obj.getdbmetadata(engine)
    spieler = datenbank_obj.spieler_dbobj(metadata)
    metadata.create_all()

#Datensatz eintragen - wenn erfasst / Fehler werden im Frontend abgefangen    
    if request.method == 'POST':
        
        conn = engine.connect()
        update = spieler.update().where(spieler.c.spielernummer==request.form['form_spielernummer']).values(aktiv=request.form['form_aktiv'])
        conn.execute(update)
        update = spieler.select()
        conn.execute(update).fetchall()

        pass
    else:
        pass
    return 


# offen komplett ist nur spielerkopieren ....
def spielerverwalten():

# anlage Datenbank - falls nicht vorhanden
    engine = create_engine('sqlite:///daten/spieler.db')

    metadata = datenbank_obj.getdbmetadata(engine)
    spieler = datenbank_obj.spieler_dbobj(metadata)
    metadata.create_all()

#Datensatz eintragen - wenn erfasst / Fehler werden im Frontend abgefangen    
    if request.method == 'POST':
        
        conn = engine.connect()
        update = spieler.update().where(spieler.c.spielernummer==request.form['form_spielernummer']).values(aktiv=request.form['form_aktiv'])
        conn.execute(update)
        update = spieler.select()
        conn.execute(update).fetchall()

        pass
    else:
        pass
    return 
#ok offen !!!!! 


def spielerkopieren():
#Anlage Datenbank - falls nicht vorhanden

    engine = create_engine('sqlite:///daten/spieler.db')
    metadata = datenbank_obj.getdbmetadata(engine)
    spieler = datenbank_obj.spieler_dbobj(metadata)
    wertzahl = datenbank_obj.wertzahl_dbobj(metadata)
    paarung = datenbank_obj.paarung_dbbj(metadata)
    aktuelle_runde = datenbank_obj.aktuellerunde_dbobj(metadata)
    
    metadata.create_all()



    if request.method == 'POST':
        suche_spieler = request.form['form_spielerid']
        spielerid_alt = suche_spieler
        p_spieler = spieler.select().where(spieler.c.spielernummer==suche_spieler)
        p_wertzahl = wertzahl.select().where(wertzahl.c.spielernummer==suche_spieler)
        p_paarung = paarung.select().where(paarung.c.spielernummer==suche_spieler)
        p_aktuelle_runde = aktuelle_runde.select().where(aktuelle_runde.c.spielernummer==suche_spieler)
        spielerid_neu=request.form['form_spieleridneu']

        #Spieler Grunddaten kopieren
        conn = engine.connect()
        result = conn.execute(p_spieler)
        var_werte = ""
        for row in result:
            var_werte = var_werte+(str(row))
        print(var_werte)
        var_werte=var_werte.replace(", '", "| '")
        var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
        var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
        var_werte=var_werte.replace("(", "")
        var_werte=var_werte.split("| ")
        print(var_werte)

        insert_spieler = spieler.insert().values(name=var_werte[1], vorname=var_werte[2], aktiv="J", spielernummer=spielerid_neu, 
        datumab=var_werte[5], ak=var_werte[6], verein=var_werte[7] , email=var_werte[8], mobil=var_werte[9], geburtsdatum=var_werte[10], uwgprivat="Nein",
        letztergegner="0", vorletztergegner="0", drittletztergegner="0", partienmitw="0", partienmits="0", patienspielfrei="0")
        engine.execute(insert_spieler)

        #Wertzahl kopieren
        conn = engine.connect()
        result = conn.execute(p_wertzahl)
        var_werte = ""
        for row in result:
            var_werte = var_werte+(str(row))
        
        var_werte=var_werte.replace(", '", "| '")
        var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
        var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
        var_werte=var_werte.replace("(", "")
        var_werte=var_werte.split("| ")
        
        insert_wertzahl = wertzahl.insert().values(spielernummer=spielerid_neu, wertzahl="600")
        engine.execute(insert_wertzahl)


        conn = engine.connect()
        result = conn.execute(p_paarung)
        var_werte = ""
        for row in result:
            var_werte = var_werte+(str(row))
        
        var_werte=var_werte.replace(", '", "| '")
        var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
        var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
        var_werte=var_werte.replace("(", "")
        var_werte=var_werte.split("| ")

        insert_paarung = paarung.insert().values(spielernummer=spielerid_neu, twz_gegner="99", brett="99", ergebnis = "99")
        engine.execute(insert_paarung)


        conn = engine.connect()
        result = conn.execute(p_aktuelle_runde)
        var_werte = ""
        for row in result:
            var_werte = var_werte+(str(row))
        
        var_werte=var_werte.replace(", '", "| '")
        var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
        var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
        var_werte=var_werte.replace("(", "")
        var_werte=var_werte.split("| ")

        insert_aktuelle_runde = aktuelle_runde.insert().values(spielernummer=spielerid_neu, aktuelles_brett="0", aktueller_gegner="0",
        aktuelle_farbe="0", aktuell_aktiv="J", aktuelle_runde="0", letztes_brett="0", letzter_gegner="0", letzte_farbe="0", letzterunde_aktiv="N", letzte_runde="0")
        engine.execute(insert_aktuelle_runde)

        pass
    else:
        pass
    return 
#ok 23092021


def spielerloeschen():
    
    if request.method == "POST":

        engine = create_engine('sqlite:///daten/spieler.db')
        metadata = datenbank_obj.getdbmetadata(engine)
        spieler = datenbank_obj.spieler_dbobj(metadata)
        wertzahl = datenbank_obj.wertzahl_dbobj(metadata)
        paarung = datenbank_obj.paarung_dbbj(metadata)
        aktuelle_runde = datenbank_obj.aktuellerunde_dbobj(metadata)

        conn = engine.connect()
        var_text=request.form['form_spielernummer']
        
        del_spieler=spieler.delete().where(spieler.c.spielernummer==request.form['form_spielernummer'])
        conn.execute(del_spieler)
        del_spieler = spieler.select()
        conn.execute(del_spieler).fetchall()

        del_wertzahl=wertzahl.delete().where(wertzahl.c.spielernummer==request.form['form_spielernummer'])
        conn.execute(del_wertzahl)
        del_wertzahl = wertzahl.select()
        conn.execute(del_wertzahl).fetchall()

        del_paarung=paarung.delete().where(paarung.c.spielernummer==request.form['form_spielernummer'])
        conn.execute(del_paarung)
        del_paarung = paarung.select()
        conn.execute(del_paarung).fetchall()

        del_aktuelle_runde=aktuelle_runde.delete().where(aktuelle_runde.c.spielernummer==request.form['form_spielernummer'])
        conn.execute(del_aktuelle_runde)
        del_aktuelle_runde = aktuelle_runde.select()
        conn.execute(del_aktuelle_runde).fetchall()


    else:
        pass    
    
    return

