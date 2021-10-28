from flask import Flask
from flask import request
import os, webbrowser, time
from flask import render_template
import setting
import spieler_mod, runden_mod

#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, MetaData, Table, DATE
from sqlalchemy.sql import select 




app = Flask(__name__)

@app.route('/')
def index():
    var_kalendertag=os.path.join(time.strftime('%d.%m.%Y'))

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    return render_template('index.html', v_heute=var_kalendertag, v_version_program=var_version_program, v_version_titel=var_version_titel)


@app.route('/spieler.html', methods=['GET', 'POST'])
def spieler():

    spieler_mod.spieler()

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    engine = create_engine('sqlite:///daten/spieler.db')
    message = engine.execute("SELECT spieler.id, spieler.spielernummer, spieler.name, spieler.vorname,  wertzahl.wertzahl, spieler.ak, spieler.verein FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    return render_template('/spieler.html', v_version_program=var_version_program, v_version_titel=var_version_titel, tabelle=message)
    #ok 23092021


@app.route('/spieleraktivieren.html', methods=['GET', 'POST'])
def spieleraktivieren():
    spieler_mod.spieleraktivieren()

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    engine = create_engine('sqlite:///daten/spieler.db')
    message = engine.execute("SELECT spieler.spielernummer, spieler.name, spieler.vorname, spieler.aktiv,  wertzahl.wertzahl, spieler.ak, spieler.verein FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    return render_template('/spieleraktivieren.html', v_version_program=var_version_program, v_version_titel=var_version_titel, tabelle=message)



@app.route('/spielerverwalten.html', methods=['GET', 'POST'])
def spielerverwalten():
    spieler_mod.spielerverwalten()

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    engine = create_engine('sqlite:///daten/spieler.db')
    message = engine.execute("SELECT spieler.spielernummer, spieler.name, spieler.vorname, spieler.aktiv,  wertzahl.wertzahl, spieler.ak, spieler.verein FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    return render_template('/spielerverwalten.html', v_version_program=var_version_program, v_version_titel=var_version_titel, tabelle=message)


@app.route('/spielerkopieren.html', methods=['GET', 'POST'])
def spielerkopieren():
    spieler_mod.spielerkopieren()
    
    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    engine = create_engine('sqlite:///daten/spieler.db') 
    message = engine.execute("SELECT spieler.id, spieler.spielernummer, spieler.name, spieler.vorname, wertzahl.wertzahl, spieler.ak, spieler.verein FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    return render_template('/spielerkopieren.html', v_version_program=var_version_program, v_version_titel=var_version_titel, tabelle=message)
    #ok 23092021 ??



@app.route('/spielerloeschen.html', methods=['GET', 'POST'])
def spielerloeschen():
    spieler_mod.spielerloeschen()

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    engine = create_engine('sqlite:///daten/spieler.db')
    message = engine.execute("SELECT spieler.spielernummer, spieler.name, spieler.vorname,  wertzahl.wertzahl, spieler.ak, spieler.verein FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    return render_template('/spielerloeschen.html', v_version_program=var_version_program, v_version_titel=var_version_titel, tabelle=message)
# ok 23092021 aber noch HTML Form


@app.route('/rundeneu.html', methods=['GET', 'POST'])
def rundeneu():
    runden_mod.rundeneu()

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    engine = create_engine('sqlite:///daten/spieler.db')
    message = engine.execute("SELECT spieler.spielernummer, spieler.name, spieler.vorname,  wertzahl.wertzahl, spieler.letztergegner, spieler.vorletztergegner, spieler.drittletztergegner, spieler.partienmitw, spieler.partienmits, spieler.patienspielfrei FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    
    return render_template('/rundeneu.html', v_version_program=var_version_program, v_version_titel=var_version_titel, tabelle=message)
    

@app.route('/ergebnis.html', methods=['GET', 'POST'])
def ergebnis_eintragen():
    runden_mod.ergebnisseintragen()

    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    twz_brett1w = "Brett1w"

    engine = create_engine('sqlite:///daten/spieler.db')
    message = engine.execute("SELECT spieler.spielernummer, spieler.name, spieler.vorname,  wertzahl.wertzahl, spieler.letztergegner, spieler.vorletztergegner, spieler.drittletztergegner, spieler.partienmitw, spieler.partienmits, spieler.patienspielfrei FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    paarungen = engine.execute("SELECT spieler.spielernummer, spieler.name, spieler.vorname,  wertzahl.wertzahl, spieler.letztergegner, spieler.vorletztergegner, spieler.drittletztergegner, spieler.partienmitw, spieler.partienmits, spieler.patienspielfrei FROM spieler INNER JOIN wertzahl ON spieler.spielernummer=wertzahl.spielernummer")
    

    return render_template('/ergebnis.html', twz_brett1w=twz_brett1w, v_version_program=var_version_program, v_version_titel=var_version_titel, tabelle=message, paarungen=paarungen)


@app.route('/')
def rundebeenden():
    runden_mod.rundebeenden()

    var_kalendertag=os.path.join(time.strftime('%d.%m.%Y'))
    var_version_titel = setting.Version_Titel
    var_version_program = setting.Version_Program

    return render_template('index.html', v_heute=var_kalendertag, v_version_program=var_version_program, v_version_titel=var_version_titel)


webbrowser.open('http://'+setting.Flask_Server_Name)
if __name__ =='__main__':
    app.run(port=17102, debug=False)
