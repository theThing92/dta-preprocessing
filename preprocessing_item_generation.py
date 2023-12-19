import csv
import random
import re

##Satz mit Target wie lang soll er sein? Satz maximal 30 Woerter lang. Erstmal alles erzeugen.
##Targetsatz sollte maximal 30 woerter lang und der Kontext soll 20 Woerter lang sein.
##Kontext ganz gross setzen. (Nur echte Worter beachten)
##Mindestlaenge 8 Maximal 30 Woerter
##In den targetsaetzen soll ein Verb vorkommen.


def correct_punct(tokenlist):
    """
    Input: Liste an Tokens
    Output: String

    Funktion De-Tokenisiert eine Liste an Tokens, editiert Einzelfälle um einen Text zu erschaffen, der einfacher zu verstehen ist
    """

    # " ".join(tokenlist) fügt jeden Eintrag der Liste einem String zu, " " (whitespace) als Trennzeichen der Einträge
    cs = " ".join(tokenlist)  # cs: corrected_string

    # Ersetzt öffnende und schließende Klammern mit Leerzeichen auf beiden Seiten durch Klammern mit dem Leerzeichen auf der geschlossenen Seite:
    # - "Sonst würde das ( ungefähr ) so aussehen"
    # - "Jetzt sieht es (ungefähr) so aus"
    cs = cs.replace(" ( ", " (")
    cs = cs.replace(" ) ", ") ")

    # Regulärer Ausdruck um die Satzzeichen [.,:;?!] mit einem Leerzeichen davor gefolgt von beliebige anderen Zeichen zu finden
    # Ersetzt die Satzzeichen mit Leerzeichen davor durch Satzzeichen ohne Leerzeichen
    # - "Das ist ein Beispielsatz . Das ist ein zweiter Beispielsatz ! Und noch ein Dritter ? "
    # - "Das ist ein Beispielsatz. Das ist ein zweiter Beispielsatz! Und noch ein Dritter? "
    cs = re.sub(r" ([.,:;?!]+)", r"\1", cs)

    # Ausgabe des Bearbeiteten Strings, .strip() entfernt Leerzeichen vor und nach dem String, dass der String immer mit einem Zeichen beginnt und endet
    return cs.strip()


def string_process(tuple_input):
    """
    Input: Tuple aus Listen mit Tokens und String, Listen beeinhalten Tokens(String), Format: Liste, Liste, String, Liste, Liste
    Output: Tuple aus Strings

    Funktion De-Tokenisiert alle Teile des Tuples (wenn erforderlich) und fügt alle Tokens aus den jeweiligen Listen in String, wobei jede Liste zu einem eigenen String
    zusammengefasst wird. Format: String, String, String, String
    """

    # Aufteilen des tuple_input in die einzelnen Bestandteile

    PS = tuple_input[0]  # pre_sentence
    PTS = tuple_input[1]  # pre_target_sentence
    T = tuple_input[2]  # target
    ATS = tuple_input[3]  # after_target_sentence
    AS = tuple_input[4]  # after_sentence

    def correct_punct(tokenlist):
        """
        Input: Liste an Tokens
        Output: String

        Funktion De-Tokenisiert eine Liste an Tokens, editiert Einzelfälle um einen Text zu erschaffen, der einfacher zu verstehen ist
        """

        # " ".join(tokenlist) fügt jeden Eintrag der Liste einem String zu, " " (whitespace) als Trennzeichen der Einträge
        cs = " ".join(tokenlist)  # cs: corrected_string

        # Ersetzt öffnende und schließende Klammern mit Leerzeichen auf beiden Seiten durch Klammern mit dem Leerzeichen auf der geschlossenen Seite:
        # - "Sonst würde das ( ungefähr ) so aussehen"
        # - "Jetzt sieht es (ungefähr) so aus"
        cs = cs.replace(" ( ", " (")
        cs = cs.replace(" ) ", ") ")

        # Regulärer Ausdruck um die Satzzeichen [.,:;?!] mit einem Leerzeichen davor gefolgt von beliebige anderen Zeichen zu finden
        # Ersetzt die Satzzeichen mit Leerzeichen davor durch Satzzeichen ohne Leerzeichen
        # - "Das ist ein Beispielsatz . Das ist ein zweiter Beispielsatz ! Und noch ein Dritter ? "
        # - "Das ist ein Beispielsatz. Das ist ein zweiter Beispielsatz! Und noch ein Dritter? "
        cs = re.sub(r" ([.,:;?!]+)", r"\1", cs)

        # Ausgabe des Bearbeiteten Strings, .strip() entfernt Leerzeichen vor und nach dem String, dass der String immer mit einem Zeichen beginnt und endet
        return cs.strip()

    # Bearbeiten der Tuple-Teile mit der oben definierten Funktion
    js_PS = correct_punct(PS)
    js_PTS = correct_punct(PTS)
    js_ATS = correct_punct(ATS)
    js_AS = correct_punct(AS)

    # Alle Teile (Strings) zu einem Tuple kombinieren und ausgeben
    joined_string = js_PS, js_PTS, T, js_ATS, js_AS

    return joined_string


""""
Input:

E2 + E2: 1000 Tuples (file1, file2)
...

Output:
15x Satzpaare mit "Zufall" aus E2+E2
15x Satzpaare mit "Zufall" aus E4+E4
30x Satzpaare mit "Zufall" aus E2+E4

15x Satzpaare mit "Kind" aus E2+E4
..."""

##Beim Output log-Datei: Ursprungstext und SatzID, aus welcher Kategorie, (z.B. E2+E2), und Targetwort##
##Woerter suchen ueber Lemma nicht Tokencorr


def get_data(csv_file, Lemma):
    """Input:
        - Korpusdateiname; string
        - Korrigierter Token (in der Tabelle "TOKENcorr"); string

    Funktion im Korpus sucht nach jeder mention des Suchwortes (TOKENcorr) und fügt dann die Ganze Zeile mit allen Daten einer Liste zu (results).
    Ist der gesamte Korpus durchsucht worden, gibt die Funktion die Liste mit allen Results weiter.

    Output:
        - Liste an Listen (2-dim Array), jeder Eintrag ist eine "Datenzeile" aus dem Korpus; 2-dim List
        - Liste an Integern, jeder Eintrag ist eine Zeilennummer von einem gefundenen Match; List
    """

    # Initialisieren von listen
    results = []
    komma_row = []
    csv_list = []
    # Öffnen der Korpus-Datei nach https://discuss.python.org/t/how-can-i-retrieve-a-specific-element-in-a-csv-file/19659/5

    with open(csv_file, encoding="UTF-8") as file_obj:
        fieldnames = ["Sent_ID", "Token_ID", "Corr_token", "Orig_token", "Lemma", "POS"]
        csv_dict = csv.DictReader(file_obj, delimiter="\t", fieldnames=fieldnames)

        for row in csv_dict:
            row_without_fieldnames = [row[fieldname] for fieldname in fieldnames]
            # print(row_without_fieldnames)
            csv_list.append(row_without_fieldnames)
        # reader_obj = csv.reader(file_obj)
        # #Iteriert durch jede unbearbeitete Zeile des Korpus
        # for raw_row in reader_obj:
        #     #print(raw_row)
        #     #Wenn die Zeile leer ist: überspringen
        #     if not raw_row:
        #         #print("skipped cause empty")
        #         continue
        #     #Hier wird die Zeile jetzt bearbeitet. split() funktioniert nicht auf leeren Zeilen, deswegen erst in diesem Schritt.
        #     row = raw_row[0].split("\t")
        #     #Wenn das erste Zeichen ein # ist: überspringen
        #     if row[0][0] == "#":
        #         #print("skipped cause #")
        #         continue
        #     ##Zeile wird als listen Element in Liste csv_list abgespeichert
        #     ##If-Bedingung weil ein Komma "," in der annotations irgendwie nicht erfasst wird und daher Zeilen in
        #     ##dem in der CSV datei ein Komma extra erzeugt.
        #     if row[2] == "":
        #         komma_row.append(row)
        #         komma_row[0].pop()
        #         komma_row[0].append(",")
        #         komma_row[0].append(",")
        #         komma_row[0].append(",")
        #         komma_row[0].append("$,")
        #         csv_list.append(komma_row[0])
        #         komma_row = []
        #     ##Ansonsten Zeile aus der Csv-Datei normal in die Liste hinzufuegen.
        #     else:
        #         csv_list.append(row)

    ##Wenn das 5. Element der Zeile dem Lemma was wir suchen entspricht wird die ganze Zeile in
    ##die Resulst-Liste gespeichert.
    for element in csv_list:
        try:
            if element[4] == Lemma:
                results.append(element)
        except Exception as e:
            print(
                f"An error occured while processing row {element} in doc {csv_file}. Skipping row."
            )
    # print(csv_list)
    # print(results)
    return csv_list, results


##Funktion zum ermitteln der Indizes ueber die später der Output gefunden wird
def get_list_number(csv_list, results):
    # Liste initialisieren, die später alle Stellen markiert an denen das Target-Wort vorkommt
    line_number = []

    # For-Schleife mit Zählervariable die durch die results-Liste iteriert. (Results-Liste enthält jeweils die Zeilen in denen unser Target-Wort drin ist
    for element in results:
        x = 0
        for row in csv_list:
            if element[1] == row[1]:
                ##Zählervariable wird als Index"Marker" gespeichert
                line_number.append(x)
            x += 1

    return line_number


##Funktion die das Targetwort und das Window vor und nach dem Target-Wort als Liste speichert
def get_window(line_number, csv_list, window_size):
    ##Die Liste mit den Zeilen der CSV wird verkleinert nur mit den Tokencorrs
    csv_word_list = []
    csv_sid_list = []
    for row in csv_list:
        csv_word_list.append(row[2])
        csv_sid_list.append(row[0])

    ##Listen werden initiiert
    target_word_list = []
    window_before = []
    window_after = []

    ##Die Listen mit den Indexmarkern wird verwendet um zu iterieren und dabei die 50 Wörter vor und nach dem Targetwort in Listen zu speichern
    for element in line_number:
        target_word_list.append(csv_word_list[element])
        before_target = int(element) - int(window_size)
        window_before.append(csv_word_list[before_target:element])
        after_target = int(element) + int(window_size) + 1
        after_element = int(element) + 1
        window_after.append(csv_word_list[after_element:after_target])

    target_sid_list = []
    window_before_sid = []
    window_after_sid = []

    ##Das gleiche mit den SIDs.
    for element in line_number:
        target_sid_list.append(csv_sid_list[element])
        before_target_sid = int(element) - int(window_size)
        window_before_sid.append(csv_sid_list[before_target_sid:element])
        after_target_sid = int(element) + int(window_size) + 1
        after_element_sid = int(element) + 1
        window_after_sid.append(csv_sid_list[after_element_sid:after_target_sid])

    return (
        target_word_list,
        window_before,
        window_after,
        target_sid_list,
        window_before_sid,
        window_after_sid,
    )


##Funktion, die den Kontext ausschneidet und Satzgrenzen anpasst
def get_sent(
    target_word_list,
    window_before,
    window_after,
    target_sid_list,
    window_before_sid,
    window_after_sid,
):
    targets = []

    ##Fuer jedes Target in der Target-wort-Liste wird folgendes ausgefuehrt:
    for target_w in range(len(target_word_list)):
        ##Verwandelt zufällig ausgewähltes Targetwort in einen String (eigentlich unnötig)
        selected_target_word = []
        selected_target_word.append(target_word_list[target_w])
        target_word = "".join(selected_target_word)

        ##Verwandelt zufällig ausgewähltes Targetwort SID in einen String
        selected_target_sid = []
        selected_target_sid.append(target_sid_list[target_w])
        target_sid = "".join(selected_target_sid)

        ##Verwandelt den entsprechneden Vor-Kontext 3D-Listen-Element in eine 2D-Liste
        selected_window_before = []
        for element in window_before[target_w]:
            selected_window_before.append(element)

        ##Verwandelt den entsprechneden Nach-Kontext 3D-Listen-Element in eine 2D-Liste
        selected_window_after = []
        for element in window_after[target_w]:
            selected_window_after.append(element)

        ##Verwandelt die entsprechneden Vor-Kontext-SIDs 3D-Listen-Element in eine 2D-Liste
        selected_window_before_sid = []
        for element in window_before_sid[target_w]:
            selected_window_before_sid.append(element)

        ##Verwandelt die entsprechneden Nach-Kontext-SIDs 3D-Listen-Element in eine 2D-Liste
        selected_window_after_sid = []
        for element in window_after_sid[target_w]:
            selected_window_after_sid.append(element)

        ##Listen fuer Vor-Kontext im Satz und ausserhalb des Satzes.
        output_before_out_sent = []
        output_before_in_sent = []

        ##Listen fuer Nach-Kontext im Satz und ausserhalb des Satzes.
        output_after_out_sent = []
        output_after_in_sent = []

        ##For Schleife mit Zaehler-Variable gleicht ab ob die Elemente in dem
        ##Vor-Kontext im Satz des Targetwort sind oder nicht und fuegt sie entsprechend getrennten Listen hinzu
        zaehler = 0
        for element in selected_window_before:
            if selected_window_before_sid[zaehler] == target_sid:
                output_before_in_sent.append(element)
            else:
                output_before_out_sent.append(element)
            zaehler += 1

        ##Das gleiche wie vorhin nur analog fuer den Nach-Kontext
        zaehler2 = 0
        for element in selected_window_after:
            if selected_window_after_sid[zaehler2] == target_sid:
                output_after_in_sent.append(element)
            else:
                output_after_out_sent.append(element)
            zaehler2 += 1

        context_and_sent = []
        ##Die Satz und Kontext Elemente werden einer Liste hinzugefuegt damit der ganze Satz und Kontext als ein Element
        ##In einer Liste steht
        context_and_sent.append(output_before_out_sent)
        context_and_sent.append(output_before_in_sent)
        context_and_sent.append(target_word)
        context_and_sent.append(output_after_in_sent)
        context_and_sent.append(output_after_out_sent)
        ##Kontext und Satz eines Vorkommens von targetswort wird als ein Element hinzugefuegt.
        targets.append(context_and_sent)

    return targets, target_sid_list


def filter_target(targets, target_sid_list):
    targets_final = []
    targets_final_sid = []
    count_sid = 0

    ##Fuer jedes Element in Targets-Liste (Ein Element in Targets_liste ist Kontext und Satz des Targetworts
    for element in targets:
        ##Zaehlt die maximale Laenge des Satzes zusammen
        max_len = len(element[1]) + len(element[3])
        ##Wenn Laenge Maximal 30 Tokens lang ist
        if max_len <= 30:
            ##Zaehlt die minimale Laenge des Satzes zusammen
            min_len = len(element[1]) + len(element[3])
            ##Und minimal 8 Tokens lang ist
            if min_len >= 8:
                ##Dann soll er den Vorkontext auf maximal 20 Tokens zuschneiden
                while len(element[0]) > 20:
                    element[0].pop(0)
                ##Und den Nach Kontext auf maximal 20 Tokens zuschneiden
                while len(element[4]) > 20:
                    element[4].pop(-1)
                ##Das Ergebnis dann in eine neue finale Liste uebergeben
                targets_final.append(element)
                ##Gleichzeitig wird von den ausgewaehlten Elementen auch das entsprechende SID mit agespeichert in einer separaten Liste
                targets_final_sid.append(target_sid_list[count_sid])
        count_sid += 1

    return targets_final, targets_final_sid


##Waehlt einen zufaelliges Vorkommen aus.
def get_random(targets_final, rand_numb, targets_final_sid):
    target_random = targets_final[rand_numb]
    target_random_sid = targets_final_sid[rand_numb]

    target_context_before = target_random[0]
    target_sent_before = target_random[1]
    target_word = target_random[2]
    target_sent_after = target_random[3]
    target_context_after = target_random[4]

    return (
        target_context_before,
        target_sent_before,
        target_word,
        target_sent_after,
        target_context_after,
        target_random_sid,
    )


"""    
def run_script():

    corpus_filename = input("Enter Corpusname: ")
    Lemma = input("Enter Targetword: ")
    window_size = 50

    
    csv_list, results = get_data(corpus_filename, Lemma)
    line_number = get_list_number(csv_list, results)

    target_word_list, window_before, window_after, target_sid_list, window_before_sid, window_after_sid = get_window(line_number, csv_list, window_size)
    targets, target_sid_list = get_sent(target_word_list, window_before, window_after, target_sid_list, window_before_sid, window_after_sid)
    targets_final, targets_final_sid = filter_target(targets, target_sid_list)

    ##Erstellung der Zufallsvariable
    ##Wenn es kein Vorkommen des Targetworts gibt Return False
    if len(targets_final) == 0:
        return False
    ##Wenn es nur ein Vorkommen gibt dann Zufallsvariable 0 zum Indexen von Position 0
    ##Und Funktion laufen lassen.
    elif len(targets_final) == 1:
        rand_numb = 0
        target_context_before, target_sent_before, target_word, target_sent_after, target_context_after, target_random_sid = get_random(targets_final, rand_numb, targets_final_sid)
    ##In allen "normalen" Faellen eine Zufallsvariable erstellen und FUnktion laufen lassen
    else:
        rand_numb = random.randint(0,len(targets_final)-1)
        target_context_before, target_sent_before, target_word, target_sent_after, target_context_after, target_random_sid = get_random(targets_final, rand_numb, targets_final_sid)

    ##Log-Info List mit Corpusname, Targetwort, und die SID des Target words.
    log_data = []
    log_data.append(corpus_filename)
    log_data.append(target_word)
    log_data.append(target_random_sid)

    print(log_data)

    print(target_context_before)
    print(target_sent_before)
    print(target_word)
    print(target_sent_after)
    print(target_context_after) 
    
"""
