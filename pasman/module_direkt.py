from .module_indirekt import *     #alles von 'module_indirekt' importieren

if args.generatepassword == True:#wenn das Argument generatepasswort true ist (was immer True ist, da das Argument zuvor immer auf True gesetzt wurde)
    args.generatepassword = generatepassword() #dann ist das Passwort die Methode generatepassword(), die ein generiertes Passwort zurückgibt

titel_datei_r = open('ti.txt', "r")#Textdatei für Titel im Modus 'r' öffnen
username_datei_r = open('us.txt', "r")#Textdatei für Username im Modus 'r' öffnen
passwort_datei_r = open('pa.txt',"r")#Textdatei für Passwort im Modus 'r' öffnen

all_titel = titel_datei_r.readlines()#Textdatei von Titel lesen
all_usernames = username_datei_r.readlines()#Textdatei von Username lesen
all_passwort = passwort_datei_r.readlines()#Textdatei vom Passwort lesen

def speichern():#EINTRÄGE WERDEN IN TEXTDATEIEN GESPEICHERT
    titel_datei_a = open('ti.txt', "a")#Textdatei für Titel im Modus "a" öffnen
    username_datei_a = open('us.txt', "a")##Textdatei für Username im Modus "a" öffnen
    passwort_datei_a = open('pa.txt', "a")#Textdatei für Passwörter im Modus "a" öffnen

    titel = args.titel #das Argument args.titel ist der Titel
    username = args.username #das Argument args.username ist der Username
    password = args.generatepassword #das Argument args.generatepassword ist das generierte Passwort

    passwortenc = enc(password) #das generierte Passwort wird encoded/verschlüsselt

    titel_datei_a.write(titel + "\n")#der eingegebene Titel wird in die Textdatei von Titeln geschrieben
    username_datei_a.write(username + '\n')#der eingegebene Username wird in die Textdatei von Usernames geschrieben
    passwort_datei_a.write(str(passwortenc) + '\n')#das generierte Passwort wird encoded/verschlüsselt in die Textdatei von Passörtern geschrieben
    titel_datei_a.close()#die Titeldatei wird geschlossen
    username_datei_a.close()#die Usernamedatei wird geschlossen
    passwort_datei_a.close()#die Passwörterdatei wird geschlossen
    print('Ihr Passwort wurde generiert und in der Zwischenablage gespeichert')#Die Info an den Benutzer
    kopieren(password)#das Passwort wird für 15 Sekunden in der Zwischenablage gespeichert

def copy():#KOPIEREN DES PASSWORTS IN DER ZWISCHENABLAGE
    if Masterpw_Eingabe():#Masterpasswort wird hier abgefragt
        if suche_titel():#es wird geschaut, ob der gesuchte Titel in der Titeltextdatei drin steht
            zeilennum = suche_titel()#zeilennnummer vom gesuchten Titel wird als zeilennum deklariert
            zeilennum = zeilennum - 1 #zeilennummer -1 nehmen, da Index bei 0 beginnt
            pasw = dec(all_passwort[zeilennum][2:-1])#passwort in der Passworttextdatei wird an der gleichen zeilennummer entschlüsselt, aber nur von Index an der Stelle 2 bis zum voletzten Index
            print('Username: ' + all_usernames[zeilennum] + 'passwort in der Zwischenablage kopiert')#username wird an der gleichen Zeilennummer aus der Usernametextdatei ausgegeben
            kopieren(pasw)#das vorher entschlüsselte Passwort wird kopiert
        elif suche_titel() == False:# in diesem Fall existiert der eingegebene Titel nicht
            print('Titel exisitert nicht! Probieren Sie ein anderes Titel')# Info an den Benutzer

def masterpas():#MASTERPASSWORT/SICHERHEITSABFRAGE ERSTELLEN BZW. ÄNDERN
    if checkfile('mp.txt') == False:#es wird geschaut, ob die Mas.Passwort Textdatei leer ist
        passwort_bedingungen()#Die Bedingungen für ein sicheres Passwort werden ausgegeben
        speichern = open('mp.txt','a')#textdatei für das Mas.Pas wird geöffnet im Modus 'a'
        passwort = hide_pasw('Geben Sie Ihr gewünschtes Masterpasswort ein:')#das Passwort muss eingegeben werden(passwort bei Eingabe wird nicht klar angezeigt)
        hash_pw = hash_maspw(passwort)#das eingegebene Passwort wird gehasht dann in String umgewandelt
        speichern.write(hash_pw)#das gehashte/in String umgewandeltes Passwort wird in der Textdatei gespeichert
        print('Ihr Passwortstärke :' + passwort_sicherheit(passwort))#Die Passwortstärke wird angezeigt
        print('Das Masterpasswort wurde gespeichert')#Info an den Benutzer
        speichern.close()#'mp.txt' schließen
        sicherheits_frage_erstellen()#die Sicherheitsfrage wird erstellt
    elif checkfile('mp.txt') == True:#in Mas.Paswort Textdatei steht bereits etwas drin/es besteht schon ein Mas.Passwort
        speichern = open('mp.txt','r')#textdatei für das Mas.Pas wird geöffnet im Modus 'r'
        maspw_txt = speichern.readlines()[0]#die erstel Zeile lesen
        Abfrage = hide_pasw('Es besteht bereits ein Masterpasswort. Geben Sie das alte Masterpassowrt ein,um ein neues Passwort zu erstellen:')#Altes Master.Pas wird abgefragt (nicht klar angezeigt)
        if masterpw_vergleich(Abfrage, maspw_txt):#es wird geschaut ob das alte Masterpasswort richtig eingegeben wurde
            if sicherheit_frage():#es wird geschaut, ob die Sicherheitsfrage richtig beantwortet wurde
                del maspw_txt #in der Mas.Passwort Textdatei wird die erste zeile gelöscht
                passwort_bedingungen()#Die Bedingungen für ein sicheres Passwort werden ausgegeben
                speichern = open('mp.txt','w')#textdatei für das Mas.Pas wird geöffnet im Modus 'w'
                neuespas = hide_pasw('Wählen Sie ein neues Passwort:')#das neue Mas.Passwort wird eingegeben (nicht klar angezeigt)
                hash_pw = hash_maspw(neuespas)#das neue Passwort wird gehasht und dann in String umgewandelt
                speichern.write(hash_pw)#das gehashte/in String umgewandeltes Passwort wird in der Textdatei gespeichert
                print('Ihr Passwortstärke :' + passwort_sicherheit(neuespas))#Die Passwortstärke wird angezeigt
                print('Das Masterpasswort wurde geändert')#Info an den Benutzer
                sicherheitfrage_neu()#neue Sicherheitsfage wird auch erstellt
                speichern.close()#'mp.txt' schließen

def display():#NACH DER RICHTIGEN EINGABE SOLLEN ALLE EINTRÄGE IN EINER TABELLE ANGEZEIGT WERDEN
    if Masterpw_Eingabe():#wenn es einen Masterpasswort gibt und der richtig eingegeben wurde dann ist die Abfrage True
        print("{:<19} {:<19} {:<19}".format('Titel', 'Username', 'Passwort'))#Tabelle wird erstellt
        print('-------------------------------------------------------')
        for i in range(0,anzahl_zeilen()):#for schleife soll solange, wie die anzahl der Zeilen in der Titeltextdatei gehe
            decpasw = dec(all_passwort[i][2:-1])#passwort wird in jeder Zeile entschlüsselt, aber nur von Index an der Stelle 2 bis zum voletzten Index
            print("{:<20}".format(all_titel[i].replace("\n","")) +#titel von jeder Zeile wird ausgegeben (nach der Ausgabe eine Zeile weiter gehen)
                  "{:<20}".format(all_usernames[i].replace("\n","")) +#username von jeder Zeile wird ausgegeben (nach der Ausgabe eine Zeile weiter gehen)
                  "{:<20}".format(decpasw))#das bereits entschlüsselte Passwort von jeder Zeile wird ausgegeben (nach der Ausgabe eine Zeile weiter gehen)

def delete():#EINTRAG KANN GELÖSCHT WERDEN
    if Masterpw_Eingabe():#wenn es einen Masterpasswort gibt und der richtig eingegeben wurde dann ist die Abfrage True
        if suche_titel() > 0:#es wird geschaut, ob der Titel exisitiert
            zeilennum = suche_titel()#Zeilennummer wird der Variable übergeben
            zeilennum = zeilennum - 1 ### Zeilennummer muss man -1 machen, da beim Löschen bei Index 0 beginnt
            Abfrage = input('Möchten Sie den Eintrag wirklich löschen? Wenn ja, dann antowrten Sie mit Ja' + '\n')#Benutzer muss löschen bestätigen
            if Abfrage == 'Ja' or Abfrage == 'ja':

                del all_titel[zeilennum]  ### Hier wird die Zeile in Titel Textdatei gelöscht
                del all_usernames[zeilennum]  ### Hier wird die Zeile in Username Textdatei gelöscht
                del all_passwort[zeilennum]  ### Hier wird die Zeile in Passwort Textdatei gelöscht

                titel_datei_w = open('ti.txt', 'w')#Titeltextdatei im Modus 'w' öffnen
                username_datei_w = open('us.txt', 'w')#Usernametextdatei im Modus 'w' öffnen
                passwort_datei_w = open('pa.txt', 'w')#Passworttextdatei im Modus 'w' öffnen
                for l in all_titel:#mit einer Schleife werden alle übrigen Titel gelesen
                    titel_datei_w.write(l)#bei jedem Durchlauf wird der Titel gespeichert
                titel_datei_w.close()#Datei schließen
                for l in all_usernames:#mit einer Schleife werden alle übrigen Username gelesen
                    username_datei_w.write(l)#bei jedem Durchlauf wird der Username gespeichert
                username_datei_w.close()#Datei schließen
                for l in all_passwort:#mit einer Schleife werden alle übrigen Passwörter gelesen
                    passwort_datei_w.write(l)#bei jedem Durchlauf wird das Passwort gespeichert
                passwort_datei_w.close()#Datei schließen
                print('Ihr Eintrag wurde gelöscht')
            else:#falls Benutzer das Löschen nicht bestätigt
                print('Ihr Eintrag wird nicht gelöscht!')
        else:#falls der Titel nicht exisitiert
            print('Der Titel exisitert nicht! Probieren Sie es noch einmal')

def Info():#INFO FÜR DEN BENUTZER, FALLS EIN UNBEKANNTER BEFEHL EINGEGEBEN WIRD
    print('PASSWORTMANAGER BEFEHLE')
    print('------------------------')
    print('Eintrag speichern: add --titel "IHR TITEL" --username "IHR USERNAME" --generatepassword')
    print('Eintrag löschen: delete --titel "TITEL EINGEBEN" ' )
    print('Passwort kopieren: copy --titel "TITEL EINGEBEN"')
    print('Alles ausgeben: display')
    print('Masterpasswort erstellen/ändern: createmasterpas')

titel_datei_r.close()#die ganz am Anfang geöffnete Textdati für Titel wird geschlossen
username_datei_r.close()#die ganz am Anfang geöffnete Textdati für Titel wird geschlossen
passwort_datei_r.close()#die ganz am Anfang geöffnete Textdati für Titel wird geschlossen