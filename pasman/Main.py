from .module_direkt import * # alles von module_direkt wird importiert


def main():#es wird geprüft, welcher Befehl vom Benutzer eingegeben wurde
    if args.befehl == 'add':
        speichern()
    elif  args.befehl == 'display':
        display()
    elif args.befehl == 'delete':
        delete()
    elif args.befehl == 'copy':
        copy()
    elif args.befehl == 'createmasterpas':
        masterpas()
    else:
        Info()

















