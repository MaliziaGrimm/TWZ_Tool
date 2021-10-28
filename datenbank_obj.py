
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, MetaData, Table, DATE


def spieler_dbobj(metadata):

    spieler = Table('spieler', metadata, 
    Column('id', Integer, primary_key=True),
    Column('name', Text),
    Column('vorname', Text),
    Column('aktiv', Text), 
    Column('spielernummer', Text),
    Column('datumab', Text),
    Column('ak', Text),
    Column('verein', Text),
    Column('email', Text),
    Column('mobil', Text),
    Column('geburtsdatum', Text),
    Column('uwgprivat', Text),
    Column('letztergegner', Text),
    Column('vorletztergegner', Text),
    Column('drittletztergegner', Text),
    Column('partienmitw', Text),
    Column('partienmits', Text),
    Column('patienspielfrei', Text)
    )
    return spieler

def wertzahl_dbobj(metadata):

    wertzahl = Table('wertzahl', metadata,
    Column('id', Integer, primary_key=True),
    Column('spielernummer', Text),
    Column('wertzahl', Text)
    )
    return wertzahl

def paarung_dbbj(metadata): 

    paarung = Table('paarung', metadata,
    Column('id', Integer, primary_key=True),
    Column('spielernummer', Text),
    Column('twz_gegner', Text),
    Column('brett', Text),
    Column('ergebnis', Text)
    )
    return paarung

def aktuellerunde_dbobj(metadata):

    aktuelle_runde = Table('aktuelle_runde', metadata,
    Column('id', Integer, primary_key=True),
    Column('spielernummer', Text),
    Column('aktuelles_brett', Text),
    Column('aktueller_gegner', Text),
    Column('aktuelle_farbe', Text),
    Column('aktuell_aktiv', Text),
    Column('aktuelle_runde', Text),
    Column('letztes_brett', Text),
    Column('letzter_gegner', Text),
    Column('letzte_farbe', Text),
    Column('letzterunde_aktiv', Text),
    Column('letzte_runde', Text)
    )
    return aktuelle_runde


def getdbmetadata(engine):

    metadata = MetaData()
    metadata.bind = engine

    return metadata
