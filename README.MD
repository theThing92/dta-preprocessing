# dta-preprocessing

## Installation
**Hinweis**: Wenn das Main Skript [preprocess_data.sh](preprocess_data.sh) direkt ausgeführt wird, ist keine
Installation notwendig. Alle notwendigen Dependenzen werden automatisch mitinstalliert.

Wird der Code aus einzelnen Modulen separat verwendet, können diese wie folgt installiert werden:

```bash
python3 -m pip install tqdm # optional
python3 -m pip install pandas # notwendig
```

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
- `-o` oder `--output_directory`: Mit dieser Option kann das Output Verzeichnis zum Speichern der XML- und Text-Dateien angegeben werden.

## Anleitung

### CLI
1. Man kann das Programm ausfuehren, indem man die Python-Datei ausfuehrt.
2. Verwende dazu die CLI-Optionen, um die gewuenschten Aktionen auszufuehren.

Beispiel:

```bash
python3 preprocessing.py -x data/xml/brockes_vergnuegen03_1730.tcf.xml
```

Dieser Befehl liest die XML-Datei `data/xml/brockes_vergnuegen03_1730.tcf.xml` ein, 
extrahiert die Daten und speichert sie in einer .txt-Datei und einem gepickelten dict.

```bash
python3 preprocessing.py -s data/xml/brockes_vergnuegen03_1730.tcf.xml
```

Dieser Befehl liest die XML-Datei `data/xml/brockes_vergnuegen03_1730.tcf.xml` ein 
und zeigt die Daten in der Konsole an, ohne sie zu speichern.

```bash
python3 preprocessing.py -x data/xml/brockes_vergnuegen03_1730.tcf.xml -o xml_extracted_data
```

Dieser Befehl liest die XML-Datei `data/xml/brockes_vergnuegen03_1730.tcf.xml` ein, 
extrahiert die Daten und speichert sie in einer .txt-Datei und einem gepickelten dict unter my/custom/directory.
 
### Modul 
Alternativ kann man die folgenden Funktionen ausfuehren:
```
from preprocessing import run_meta_data_extraction
file_path: str = "data/xml/brockes_vergnuegen03_1730.tcf.xml"
run_meta_data_extraction(file_path)
```

### Beispiel-Output
```
#author_surname=Mommsen
#author_forename=Theodor
#pub_name=Mommsen, Theodor: Römische Geschichte. Bd. 3: Von Sullas Tode bis ....
#pub_place=Leipzig
#pub_date=1856
#textClass_DTACorpus=core,ready,mts
#textClass_dtamain=Fachtext
#textClass_dtasub=Historiographie
#textClass_dwds1main=Wissenschaft
#textClass_dwds1sub=Historiographie
```

### Vorverarbeitung der Daten mit multiprocessing
Die DTA Input Daten in einem Verzeichnis können parallel verarbeitet werden. Für mögliche Optionen des Skripts, siehe:
```bash
python3 process_documents.py --help
```

Ausführung der gesamten Vorverarbeitungspipeline:
```bash
./preprocess_data.sh
```
Konfigurationsparameter (Anzahl Items, Pfade zu Input-/Output-Dateien) können in den entsprechenden Variablen des Skripts gesetzt werden.

**Hinweis**:  
Für die Fortschrittsanzeige bei Generierung der Items wird in [item_generation.py](item_generation.py)
[tqdm](https://tqdm.github.io/docs/tqdm/) verwendet. Das Tool wird automatisch bei Ausführung des Skripts via pip3 installiert.
Falls dies nicht gewünscht sein sollte, kann Z. 3 in [preprocess_data.sh](preprocess_data.sh) auskommentiert werden.

# Gruppe 
- Maurice Vogel
- Christopher Chandler 
