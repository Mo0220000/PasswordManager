import random
import base64
import pyperclip
import time
import os
import argparse
import bcrypt
import stdiomask

parser = argparse.ArgumentParser(description='Befehl eingeben')#Argument wird beschrieben

parser.add_argument('befehl',help='z.B add,copy,delete,createmasterpas,display')#postionales Argument für den Befehl

parser.add_argument('-t', '--titel', help='titelname')#optionales Argument für den Titel
parser.add_argument('-u', '--username', help='username')#optionales Argument für den Username
parser.add_argument('-g', '--generatepassword',action='store_true', help='passwort wird automatisch generiert')#optionales Argument für das Passwort
#Argument für das Passwort wird auf True gesetzt, da Passwort keinen Inhalt hat, da automatisch generiert werden muss:
#In module_direkt File wird das Argument für das Passwort mit der Methode 'generatepassword()' gleichgesetzt, wodurch dann immer automatisch ein Passwort generiert wird
args = parser.parse_args()#Argumente werden übergeben

def generatepassword():#PASSWORT WIRD GENERIERT
   auswahl = ''#leerer String wird deklariert
   Abfrage_laenge = input('Wie lange soll Ihr Passwort sein?' + '\n')# länge des Passworts Benutzer
   print('Woraus soll Ihr Passwort bestehen?')
   print('Für Alle Zeichen schreiben Sie: 1')
   print('Nur Großbuchstaben schreiben Sie: 2')
   print('Nur Kleinbuchstaben schreiben Sie: 3')
   print('Nur Zahlen oder Sonderzeichen schreiben Sie: 4')
   Abfrage = input('Wählen Sie eine Zahl' + '\n')# Zeichen des Passworts durch Benutzer
   chars_alle = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.,-_#+><?!"§$%&/()='
   chars_klein = 'abcdefghijklmnopqrstuvwxyz'
   chars_groß = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
   chars_zahlen_sonderzeichen = '1234567890.,-_#+><?!"§$%&/()='
   if Abfrage == '1':# wenn Benutzereingabe 1, dann alle chars nutzen
      auswahl = chars_alle
   elif Abfrage == '2':# wenn Benutzereingabe 2, dann nur Großbuchstaben nutzen
      auswahl = chars_groß
   elif Abfrage == '3':# wenn Benutzereingabe 3, dann nur Kleinbuchstaben nutzen
      auswahl = chars_klein
   elif Abfrage == '4':# wenn Benutzereingabe 4, dann nur Zahlen und Sonderzeichen nutzen
      auswahl = chars_zahlen_sonderzeichen
   Passwort = "" #leerer String wird deklariert

   for x in range(0, int(Abfrage_laenge)):# for schleife je nachdem welche Länge der Nutzer ausgewählt hat
      passwort_zeichen = random.choice(auswahl)#mit random Passwort erstllen: nur Zeichen, die der Nutzer ausgewählt hat
      Passwort += passwort_zeichen#für jeden Durchlauf wird ein char hinzugefügt
   return Passwort# Passwort wird zurückgegeben

def enc(pasw):#PASSWORT VERSCHLÜSSELN - pasw ist dann das generierte Passwort
   password = base64.b64encode(pasw.encode("utf-8"))#das generierte Passwort wird encoded/verschlüsselt
   return password#das verschlüsselte Passwort wird zurückgegeben

def dec(encpas):#PASSWORT ENTSCHLÜSSELN - encpas ist das bereits verschlüsselte Passwort
   decpas = base64.b64decode(encpas).decode(("utf-8")) # das verschlüsselte Passwort wird decoded/entschlüsselt
   return decpas#das entschlüsselte Passwort wird zueückgegeben

def kopieren(password):#PASSWORT KOPIEREN - password ist das entschlüsselte Passwort
   pyperclip.copy(password) # das Passwort wird kopiert
   if os.fork() == 0:# Kindprozess wird erstellt, der immer True ist, und unabhängig vom Eltrnprozess läuft
      time.sleep(15)# 15 Sekunden passiert dann nichts (Zeit friert dann ein)
      if pyperclip.paste() == password:#wenn dann in der Zwischenablage immer noch das Passwort steht:
         pyperclip.copy('')#dann soll nichts kopiert werden, somit ist die Zwischenablage wieder leer

def suche_titel():#SUCHE TITEL IN TEXTDATEI
   search = args.titel# die suche ist das Argument titel
   with open('ti.txt') as f:#Textdatei wird als f geöffnet
      for num, line in enumerate(f, 1):#in einer for schleife wird jede Zeile durchgegangen
         if search in line:#wenn Titel in der Zeile gefunden wird
           return int(num)#dann soll die Zeilennummer zurückgegeben werden
   return False

def anzahl_zeilen():#ANZAHL DER ZEILEN IN EINER TEXTDATEI RAUSFINDEN
   with open('ti.txt') as myfile:# die Textdatei wird als myfile geöffnet
      anzahl_zeilen_titel = sum(1 for line in myfile)#mit einer For Schleife wird die Anzahl der Zeilen ermittelt
   return anzahl_zeilen_titel

def hash_maspw(Eingabe):#DAS PASSWORT HASHEN/VERSCHLÜSSELN - die Eingabe ist das eigegebene Mas.Passwort
   hashed_password = bcrypt.hashpw(Eingabe.encode('utf8'), bcrypt.gensalt())#Passwort wird hier gehasht
   # convert to string with correct format
   string_password = hashed_password.decode('utf8')#das gehashte Passwort in String umwandeln
   return string_password#das in String umgewandelte Passwort wird zurückgegeben

def hide_pasw(prompt):#PASSWORT NICHT KLAR ANZEIGEN
   Eingabe = stdiomask.getpass(prompt=prompt + '\n', mask='*')#prompt ist dann die Abfrage und das Pasw. wird als "*" angezeigt
   return Eingabe # das eingegebene soll zurückgegeben werden

def checkfile(filename):#STEHT IN EINER  DATEI ETWAS DRIN?
   if os.stat(filename).st_size > 0:#wennn in filename etwas drin steht, dann ist size größer 0
      return True # True soll zurückgegeben werden
   else:# wenn nichts im filename drin steht
      print('Es besteht kein Masterpasswort:')
      print('Erstellen Sie ein Masterpasswort mit dem Befehl: createmasterpas')

def masterpw_vergleich(Eingabe, string_password):#EINGABE MIT MAS.PASSWORT VERGLEICHEN
   check = bcrypt.checkpw(Eingabe.encode('utf8'), string_password.encode('utf8'))#die Eingabe vom Benutzer wird mit dem gehashten Passwort, der in String umgewandelt wurde verglichen
   if check == True:#wenn der Vergleich identisch ist, dann wird True zurückgegeben
      return True
   else:#ansonsten wurde das Passwort falsch eingegeben
      print('Das Masterpasswort wurde falsch eingegeben. Probieren Sie es noch einmal')

def Masterpw_Eingabe():#GIBT ES EINEN MASPASSWORT? WENN JA, WURDE DER RICHTIG EINGEGEBEN?
   if checkfile('mp.txt'):# steht in der mp.txt Datei etwas drin?
      maspw_txt = open('mp.txt', 'r')#die Datei im Modus 'r' wird geöffnet
      maspw_txt_lesen = maspw_txt.readlines()[0]#die erste Zeile wird gelesen
      Eingabe = hide_pasw('Bitte geben Sie das Masterpassword ein:')#die Passworteingabe wird nicht klar angezeigt
      if masterpw_vergleich(Eingabe, maspw_txt_lesen):#Passworteingabe mit Mas.Passwort aus Textdatei vergleichen
         return True#wenn richtig, soll True zurückgegeben werden

def sicherheits_frage_erstellen():#EINE SICHERHEITSFRAGE ERSTELLEN
   frage_txt = open('frage.txt', 'w')#Textdatei für Frage wird geöffnet im Modus'w'
   antwort_txt = open('antwort.txt', 'w')#Textdatei für Antwort wird geöffnet im Modus 'w'
   Frage = input('Wie soll die Sicherheitsfrage lauten?'+ '\n')#Frage wird vom Benutzer eingegeben
   frage_txt.write(Frage)#Frage wird in 'frage.txt' gespeichert
   Antwort = input('Was ist die Antwort zu Ihrer Frage?' + '\n')#Antwort wird vom Benutzer eingegeben
   antwort_txt.write(Antwort)#Antwort wird in 'antwort.txt' gespeichert
   print('Ihre Eingaben wurden gespeichert')#Info an den n Benutzer
   frage_txt.close()#'frage.txt' schließen
   antwort_txt.close()#'antwort.txt' schließen

def sicherheit_frage():#SICHERHEITSFRAGE ABFRAGEN
   frage_txt = open('frage.txt','r')#Textdatei für Frage wird geöffnet im Modus 'r'
   antwort_txt = open('antwort.txt', 'r')#Textdatei für Antwort wird geöffnet im Modus 'r'
   frage_txt_lesen = frage_txt.readlines()[0]#die erste Zeile aus der Fragentextdatei lesen
   antwort_txt_lesen = antwort_txt.readlines()[0]#die erste Zeile aus der Antwortentextdatei lesen
   print(frage_txt_lesen)#Frage wird dem Benutzer angezeigt
   Eingabe = input('Bitte beantworten Sie die Frage' + '\n')#Benutzer kann Antwort eingeben
   if Eingabe == antwort_txt_lesen:#wenn Benutzereingabe mit der Antwort aus der Textdatei identisch
       return True#dann soll true zurückgegeben werden
   else:#ansonsten war die Antwort/Eingabe vom Benutzer nicht identisch
      print('Die Sicherheitsfrage wurde falsch beantwortet')
   frage_txt.close()#'frage.txt' schließen
   antwort_txt.close()  # 'antwort.txt' schließen

def sicherheitfrage_neu():#ALTE SICHERHEITSFRAGE LÖSCHEN UND EINE NEUE ERSTELLEN
   frage_txt = open('frage.txt','r')#Textdatei für Fragen öffnen im Modus'r'
   antwort_txt = open('antwort.txt', 'r')#Textdatei für Antowrten öffnen im Modus'r'
   del frage_txt.readlines()[0]#Zeile 1 in Fragentextdatei löschen
   del antwort_txt.readlines()[0]#Zeile 1 in Antowrttextdatei löschen
   sicherheits_frage_erstellen()# mit der Methode 'sicherheits_frage_erstellen()' neue Sicherheitsfrage erstellen
   frage_txt.close()  # 'frage.txt' schließen
   antwort_txt.close()  # 'antwort.txt' schließen

def passwort_sicherheit(passwort):#PASSWORTSTÄRKE WIRD DEM BENUTZER ANGEZEIGT
   sicherheit = ''
   if len(passwort) >= 8 :#erste Bedingung: Passwort muss mindestens 8 Zeichen lang sein
      sicherheit = sicherheit + '*' # die Sicherheit ist dann: *
      if any(x.isupper() for x in passwort):#zweite Bedingung: Passwort muss mindestens einen Großbuchstaben enthalten
         sicherheit = sicherheit + '*' # Sicherheit bekommt einen weiteren *
         if any(x.isdigit() for x in passwort): #dritte Bedingung: Passwort muss mindestens eine Zahl enthalten
            sicherheit = sicherheit + '*'# Sicherheit bekommt einen weiteren *
   else:# ansonsnten ist das Passwort unsicher
      sicherheit = ' unsicher'#Sicherheit ist dann unsicher
   return sicherheit#die Sicherheit wird zurückgegeben

def passwort_bedingungen():#INFO FÜR DIE ERSTELLUNG EINES SICHEREN MASTERPASSWORTS
   print('Ihr Masterpasswort kriegt jeweils ein * für jede erfüllte Bedingung: ')
   print('Bedingung 1 : Das Passwort muss mindestens aus 8 Zeichen bestehen')
   print('Bedingung 2 : Das Passwort muss einen Großbuchstaben enthalten')
   print('Bedingung 3 : Das Passwort muss mindestens eine Zahl enthalten')
   print('Wenn keines der Bedingungen erfüllt ist, ist das Passwort unsicher')







