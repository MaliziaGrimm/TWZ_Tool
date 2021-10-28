from flask import Flask
from flask import request
import os, time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, MetaData, Table, DATE
from sqlalchemy.sql import select 

import datenbank_obj

def rundeneu():
 
    engine = create_engine('sqlite:///daten/spieler.db')

    metadata = datenbank_obj.getdbmetadata(engine)
    spieler = datenbank_obj.spieler_dbobj(metadata)
    wertzahl = datenbank_obj.wertzahl_dbobj(metadata)
    paarung = datenbank_obj.paarung_dbbj(metadata)
    aktuelle_runde = datenbank_obj.aktuellerunde_dbobj(metadata)
    
    metadata.create_all()


    if request.method == 'POST':

        i = 0
        while i < 10:
            i = i + 1

            if request.form['form_brett'+str(i)+'w'] == "" and request.form['form_brett'+str(i)+'s'] == "":
                # beide leer nichts machen
                pass

            elif request.form['form_brett'+str(i)+'w'] == "" and request.form['form_brett'+str(i)+'s'] != "":

                print("schwarz spielfrei")

                var_bw = "spielfrei"
                var_bs = request.form['form_brett'+str(i)+'s']
            
                p = spieler.select().where(spieler.c.spielernummer==var_bs)
                conn = engine.connect()
                result = conn.execute(p)
                var_werte = ""
                for row in result:
                    var_werte = var_werte+(str(row))
                var_werte=var_werte.replace(")(", ", ")
                var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
                var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
                var_werte=var_werte.replace("(", "")
                var_werte=var_werte.split(", ")
                
                var_anzspielfrei = int(var_werte[17])+1
                var_anzspielfrei = str(var_anzspielfrei)
                
                conn = engine.connect()
                spielerupdate = spieler.update().where(spieler.c.spielernummer==var_bs).values(letztergegner=var_bw, vorletztergegner=var_werte[12], drittletztergegner=var_werte[13], patienspielfrei=var_anzspielfrei)
                conn.execute(spielerupdate)
                spielerupdate = spieler.select()
                conn.execute(spielerupdate).fetchall()
                pass

            elif request.form['form_brett'+str(i)+'w'] != "" and request.form['form_brett'+str(i)+'s'] == "":
              
                print("weiß spielfrei")

                var_bs = "spielfrei"
                var_bw = request.form['form_brett'+str(i)+'w']
            
                p = spieler.select().where(spieler.c.spielernummer==var_bw)
                conn = engine.connect()
                result = conn.execute(p)
                var_werte = ""
                for row in result:
                    var_werte = var_werte+(str(row))
                var_werte=var_werte.replace(")(", ", ")
                var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
                var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
                var_werte=var_werte.replace("(", "")
                var_werte=var_werte.split(", ")
                
                var_anzspielfrei = int(var_werte[17])+1
                var_anzspielfrei = str(var_anzspielfrei)
                
                conn = engine.connect()
                spielerupdate = spieler.update().where(spieler.c.spielernummer==var_bw).values(letztergegner=var_bs, vorletztergegner=var_werte[12], drittletztergegner=var_werte[13], patienspielfrei=var_anzspielfrei)
                conn.execute(spielerupdate)
                spielerupdate = spieler.select()
                conn.execute(spielerupdate).fetchall()
                


                pass


            else:
                # kein spielfrei = normale Paarung
                # Spieler w und s einlesen                
                var_bs = request.form['form_brett'+str(i)+'s']
                var_bw = request.form['form_brett'+str(i)+'w']



                p = aktuelle_runde.select().where(aktuelle_runde.c.spielernummer==var_bw)
                conn = engine.connect()
                result = conn.execute(p)
                var_werte = ""
                for row in result:
                    var_werte = var_werte+(str(row))
                var_werte=var_werte.replace(")(", ", ")
                var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
                var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
                var_werte=var_werte.replace("(", "")
                var_werte=var_werte.split(", ")
#                # Partien mit w um 1 erhöhen
#                var_anzw = int(var_werte[15])+1
#                var_anzw = str(var_anzw)

                print(var_werte)
    #aktuelle_runde = Table('aktuelle_runde', metadata,
    #Column('id', Integer, primary_key=True),
    #Column('spielernummer', Text),
    #Column('aktuelles_brett', Text),
    #Column('aktueller_gegner', Text),
    #Column('aktuelle_farbe', Text),
    #Column('aktuell_aktiv', Text),
    #Column('aktuelle_runde', Text),
    #Column('letztes_brett', Text),
    #Column('letzter_gegner', Text),
    #Column('letzte_farbe', Text),
    #Column('letzterunde_aktiv', Text),
    #Column('letzte_runde', Text)                

                conn = engine.connect()
  unsauber !!!!              aktuelle_rundeupdate = aktuelle_runde.update().where(spieler.c.spielernummer==var_bw).values(aktuellergegner=var_bs, vorletztergegner=var_werte[12], drittletztergegner=var_werte[13], partienmitw=var_anzw )
                conn.execute(aktuelle_rundeupdate)
                aktuelle_rundeupdate = aktuelle_runde.select()
                conn.execute(aktuelle_rundeupdate).fetchall()

                
                p = spieler.select().where(spieler.c.spielernummer==var_bw)
                conn = engine.connect()
                result = conn.execute(p)
                var_werte = ""
                for row in result:
                    var_werte = var_werte+(str(row))
                var_werte=var_werte.replace(")(", ", ")
                var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
                var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
                var_werte=var_werte.replace("(", "")
                var_werte=var_werte.split(", ")
                # Partien mit w um 1 erhöhen
                var_anzw = int(var_werte[15])+1
                var_anzw = str(var_anzw)
                
                conn = engine.connect()
                spielerupdate = spieler.update().where(spieler.c.spielernummer==var_bw).values(letztergegner=var_bs, vorletztergegner=var_werte[12], drittletztergegner=var_werte[13], partienmitw=var_anzw )
                conn.execute(spielerupdate)
                spielerupdate = spieler.select()
                conn.execute(spielerupdate).fetchall()

                p = spieler.select().where(spieler.c.spielernummer==var_bs)
                conn = engine.connect()
                result = conn.execute(p)
                var_werte = ""
                for row in result:
                    var_werte = var_werte+(str(row))
                var_werte=var_werte.replace(")(", ", ")
                var_werte=var_werte.replace("'", "") # muss präzisiert werden wegen Hochkomma im Namen
                var_werte=var_werte.replace(")", "") # muss präzisiert werden wegen Klammer im Text und ähnliches
                var_werte=var_werte.replace("(", "")
                var_werte=var_werte.split(", ")
                # Partien s um 1 erhöhen
                var_anzs = int(var_werte[16])+1
                var_anzs = str(var_anzs)

                spielerupdate = spieler.update().where(spieler.c.spielernummer==var_bs).values(letztergegner=var_bw, vorletztergegner=var_werte[12], drittletztergegner=var_werte[13], partienmits=var_anzs)
                conn.execute(spielerupdate)
                spielerupdate = spieler.select()
                conn.execute(spielerupdate).fetchall()

                pass

        else:
            pass
    return 
#sollte erst mal stimmen für manuelle Auslosung




# offen --- aktuell
def ergebnisseintragen():
# anlage Datenbank - falls nicht vorhanden
    engine = create_engine('sqlite:///daten/spieler.db')

    metadata = datenbank_obj.getdbmetadata(engine)
    spieler = datenbank_obj.spieler_dbobj(metadata)
    wertzahl = datenbank_obj.wertzahl_dbobj(metadata)
    paarung = datenbank_obj.paarung_dbbj(metadata)
    aktuelle_runde = datenbank_obj.aktuellerunde_dbobj(metadata)
    

    # metadata = getdbmetadata(engine)
    # spieler = spieler_dbobj(metadata)
    # wertzahl = wertzahl_dbobj(metadata)
    # paarung = paarung_dbbj(metadata)

    metadata.create_all()

    #paarungen = engine.execute("SELECT spieler.spielernummer, spieler.name, spieler.vorname,  wertzahl.wertzahl, spieler.letztergegner, spieler.vorletztergegner, spieler.drittletztergegner, spieler.partienmitw, spieler.partienmits, spieler.patienspielfrei FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")


#Datensatz eintragen - wenn erfasst / Fehler werden im Frontend abgefangen    
    if request.method == 'POST':
        """
        insert_spieler = spieler.insert().values(name=request.form['form_name'], vorname=request.form['form_vorname'], aktiv="j", spielernummer=request.form['form_spielernummer'],
        datumab=request.form['form_eintrittsdatum'], ak=request.form['form_ak'], verein=request.form['form_verein'], email=request.form['form_email'], mobil=request.form['form_mobil'],
        geburtsdatum=request.form['form_geburtsdatum'], uwgprivat=request.form['form_uwgprivat'])
        engine.execute(insert_spieler)
        insert_wertzahl = wertzahl.insert().values(spielernummer=request.form['form_spielernummer'], wertzahl=request.form['form_twz'])
        engine.execute(insert_wertzahl)
        """
        pass
    else:
        pass
    return 
#ok offen !!!!! 

def rundebeenden():

    # hier kommt die TWZ Berechnung

    pass