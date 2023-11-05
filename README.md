# dta-preprocessing

## Beschreibung
Dieses Programm liest eine XML-Datei von der DTA (Digitale Texte und Editionen) 
und extrahiert die erforderlichen Daten aus dieser Datei. 
Die Daten werden dann sowohl als .txt-Datei als auch als gepickeltes dict gespeichert. 

Die folgenden Datenpunkte werden gespeichert:
- Autor: Vorname und Nachname
- Veroeffentlichungsort
- Veroeffentlichungsdatum
- Veroeffentlichungsname
- Textklassifikationen (gemaess den im Ressourcenverzeichnis spezifizierten XML-Tags)

## Verwendung
Um das Programm auszufuehren, kann man die folgenden Befehlszeilenoptionen verwenden:

- `-x` oder `--extract_data`: Mit dieser Option kann man eine XML-Datei einlesen
und die Daten extrahieren und speichern.
- `-s` oder `--show_data`: Mit dieser Option kann man eine XML-Datei einlesen
und die Daten anzeigen, ohne sie zu speichern.

## Anleitung

### CLI
1. Man kann das Programm ausfuehren, indem man die Python-Datei ausfuehrt.
2. Verwende dazu die CLI-Optionen, um die gewuenschten Aktionen auszufuehren.

Beispiel:

```bash
python preprocessing.py -x data/xml/brockes_vergnuegen03_1730.tcf.xml
```

Dieser Befehl liest die XML-Datei `meine_xml_datei.xml` ein, 
extrahiert die Daten und speichert sie in einer .txt-Datei und einem gepickelten dict.

```bash
python preprocessing.py -s data/xml/brockes_vergnuegen03_1730.tcf.xml
```

Dieser Befehl liest die XML-Datei `data/xml/brockes_vergnuegen03_1730.tcf.xml` ein 
und zeigt die Daten in der Konsole an, ohne sie zu speichern.
 
### Modul 
Alternativ kann man die folgenden Funktionen ausfuehren:
```
file_path: str = "data/xml/brockes_vergnuegen03_1730.tcf.xml"
run_meta_data_extraction(file_path)
```

# Gruppe 
- Maurice Vogel
- Christopher Chandler 