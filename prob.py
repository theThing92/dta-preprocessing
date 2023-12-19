import os


# Diese Methode initiiert eine Datei, in die wir unsere formatierten Versuchsitems schreiben,
# und ein log für diese Datei
def initiate(log_name):
    versuchsitems = open("data/fods/versuchsitems.txt", "w", encoding="utf-8")
    versuchsitems.write("")
    versuchsitems.close()
    logfile = open(log_name, "w", encoding="utf-8")
    logfile.write("File_S1,Lemma1,S_ID_S1,Period1,File_S2,Lemma2,S_ID_S2,Period2")
    logfile.close()


# Diese Methode bekommt unsere Metadaten für je ein Versuchsitem als Input und schreibt dafür einen Eintrag in unser log
def log_entry(
    log_name, file_s1, lemma_s1, s_id_s1, period1, file_s2, lemma_s2, s_id_s2, period2
):
    logfile = open(log_name, "a", encoding="utf-8")
    logfile.write(
        "\n"
        + file_s1
        + ","
        + lemma_s1
        + ","
        + s_id_s1
        + ","
        + period1
        + ","
        + file_s2
        + ","
        + lemma_s2
        + ","
        + s_id_s2
        + ","
        + period2
    )
    logfile.close()


# Diese Methode erzeugt eine neue Tabellenzeile inkl. linker Satz, Dropdown, rechter Satz,
# und schreibt diese Tabellenzeile in unsere Datei mit Tabellenzeilen
def create_tablerow(
    string11,
    string12,
    target1,
    string13,
    string14,
    string21,
    string22,
    target2,
    string23,
    string24,
    row_number,
):
    whitespace = " "
    # Datei öffnen
    versuchsitems = open("data/fods/versuchsitems.txt", "a", encoding="utf-8")
    # Tabellenzeile initiieren
    versuchsitems.write('    <table:table-row table:style-name="ro2">\n')
    # Linkes Feld
    versuchsitems.write(
        '     <table:table-cell table:style-name="ce5" office:value-type="string" calcext:value-type="string"><text:p><text:span text:style-name="T1">'
        + string11
        + whitespace
        + "</text:span>"
        + string12
        + whitespace
        + '<text:span text:style-name="T2">'
        + target1
        + whitespace
        + "</text:span>"
        + string13
        + whitespace
        + '<text:span text:style-name="T1">'
        + string14
        + "</text:span></text:p>\n"
    )
    versuchsitems.write("     </table:table-cell>\n")
    # Dropdown
    versuchsitems.write(
        '     <table:table-cell table:content-validation-name="val1"/>\n'
    )
    # Rechtes Feld
    versuchsitems.write(
        '     <table:table-cell table:style-name="ce5" office:value-type="string" calcext:value-type="string"><text:p><text:span text:style-name="T1">'
        + string21
        + whitespace
        + "</text:span>"
        + string22
        + whitespace
        + '<text:span text:style-name="T2">'
        + target2
        + whitespace
        + "</text:span>"
        + string23
        + whitespace
        + '<text:span text:style-name="T1">'
        + string24
        + "</text:span></text:p>\n"
    )
    versuchsitems.write("     </table:table-cell>\n")
    # Tabellenzeile abschließen
    versuchsitems.write("    </table:table-row>\n")
    versuchsitems.close()


# Hier erstellen wir aus unserer Datei mit den formatierten Tabellenzeilen mit Versuchsitems
# und zwei weiteren Dateien mit fods-Code unsere fertige fods Datei.
def merge_to_fods(fods_name):
    # als erstes die Datei leeren (damit ich das beim Testen nicht jedes Mal von Hand machen muss)
    fods = open(fods_name, "w", encoding="utf-8")
    fods.write("")
    # die Dateien öffnen, aus denen wir unsere fertige Datei zusammensetzen wollen
    fods_1 = open("data/fods/fods_1sthalf_dropdown_umlaute.txt", "r", encoding="utf-8")
    versuchsitems = open("data/fods/versuchsitems.txt", "r", encoding="utf-8")
    fods_2 = open("data/fods/fods_2ndhalf.txt", "r", encoding="utf-8")
    fods = open(fods_name, "a+", encoding="utf-8")
    # Inhalt der drei Dateien in unsere Zieldatei (fods) schreiben.
    # Die ist dann eine vollständige fods-Datei, die wir ganz normal in LibreOffice öffnen und bearbeiten können.
    fods.write(fods_1.read())
    fods.write(versuchsitems.read())
    fods.write(fods_2.read())
    # Alles schließen
    fods.close()
    fods_1.close()
    versuchsitems.close()
    fods_2.close()


def main():
    # Beispielliste zum Testen generieren (hier stattdessen die richtige übergeben!)
    input_list = make_a_dummy_list()
    # Diese Methode ruft die anderen Methoden in der richtigen Reihenfolge auf und kümmert sich um alles
    # Man muss ihr nur die Liste von Sophia übergeben
    fods_builder(input_list)


# Erstellt eine Liste beliebiger Länge, die so formatiert ist wie unsere echten Input-Listen
def make_a_dummy_list():
    beispielliste = []
    # Achtung: a ist immer ein Satz, nicht ein SatzPAAR/Versuchsitem! Also die Liste schön lang machen.
    a = 1
    while a < 50:
        beispielliste.append(
            (
                ("NUMMER: " + str(a) + "! ", "zwei", "drei", "vier", "fünf"),
                ["weigel", "adam", "s31a", "E2"],
            )
        )
        a = a + 1
    return beispielliste


# Diese Methode ruft unsere anderen Methoden in der richtigen Reihenfolge auf
def fods_builder(
    input_list,
    output_dir="./",
    pairs_per_file=5,
):
    # Wie viele Satzpaare wir pro Datei haben wollen (für Testzwecke nur 5)
    # Hier könnten wir angeben, wie wir unsere fods-Dateien und logs nennen wollen.
    # Da wird dann später automatisch eine Nummer und die Endung angehängt.
    fods_name_prefix = os.path.join(output_dir, "semchange_")
    log_name_prefix = os.path.join(output_dir, "semchange_log_")

    # Der Listeneintrag, bei dem wir gerade sind
    n = 0
    # Die Nummer der aktuellen fods-Datei, in die wir schreiben
    file_no = 1
    # Obergrenze, nach der wir eine neue Datei aufmachen oder aufhören sollen
    treshold = pairs_per_file * 2 * file_no
    # Während die Obergrenze nicht über die Länge der Input-Liste hinausgeht, tue folgendes:
    while treshold < (len(input_list) - 1):
        # Während wir aktuell unter der Obergrenze sind und unsere Obergrenze nicht zu weit über die
        # Länge der Liste hinausgeht...
        # (damit unser letztes File zwar kleiner als die anderen sein darf, aber nicht leer ist)
        while n < treshold and treshold < (len(input_list) + pairs_per_file):
            # Neue Dateinamen bestimmen
            log_name = log_name_prefix + str(file_no) + ".annotations"
            fods_name = fods_name_prefix + str(file_no) + ".fods"
            # Dateien initiieren
            initiate(log_name)
            # diese Variable zählt für uns, wie viele Versuchsitems schon im File sind
            already_in_file = 0
            while already_in_file < (pairs_per_file) and n < (len(input_list) - 2):
                # Den Elementen aus der Liste Bedeutungen zuweisen
                # Erster Satz (erster Tupel)
                string11 = input_list[n][0][0]
                string12 = input_list[n][0][1]
                target1 = input_list[n][0][2]
                string13 = input_list[n][0][3]
                string14 = input_list[n][0][4]
                # Metadaten erster Satz
                file_s1 = input_list[n][1][0]
                lemma_s1 = input_list[n][1][1]
                s_id_s1 = input_list[n][1][2]
                period1 = input_list[n][1][3]
                # Zweiter Satz (zweiter Tupel)
                string21 = input_list[n + 1][0][0]
                string22 = input_list[n + 1][0][1]
                target2 = input_list[n + 1][0][2]
                string23 = input_list[n + 1][0][3]
                string24 = input_list[n + 1][0][4]
                # Metadaten zweiter Satz
                file_s2 = input_list[n + 1][1][0]
                lemma_s2 = input_list[n + 1][1][1]
                s_id_s2 = input_list[n + 1][1][2]
                period2 = input_list[n + 1][1][3]
                row_number = n + 1
                timeperiods = "13"  # von wo kriegen wir die?
                # Tabellenzeile aus diesen beiden Sätzen erzeugen
                create_tablerow(
                    string11,
                    string12,
                    target1,
                    string13,
                    string14,
                    string21,
                    string22,
                    target2,
                    string23,
                    string24,
                    row_number,
                )
                # Eintrag im log erzeugen
                log_entry(
                    log_name,
                    file_s1,
                    lemma_s1,
                    s_id_s1,
                    period1,
                    file_s2,
                    lemma_s2,
                    s_id_s2,
                    period2,
                )
                # Variablen hochzählen (n um zwei, weil wir für ein Versuchsitem ja immer die nächsten zwei Sätze/Tupel brauchen
                n = n + 2
                already_in_file = already_in_file + 1
            # Wenn wir genug Versuchsitems haben, stellen wir unsere fods-Datei fertig
            merge_to_fods(fods_name)
            # Dann setzen wir die Obergrenze für die nächste Datei
            treshold = treshold + (pairs_per_file * 2)
            # Und setzen die Datei/log-Nr eins hoch.
            file_no = file_no + 1


if __name__ == "__main__":
    main()
