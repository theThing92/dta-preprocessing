# bei Fragen: Max.Schellenberg@ruhr-uni-bochum.de

import random
import sys
import traceback

import preprocessing_item_generation as TG

_PYTHON_VERSION = sys.version_info

try:
    from tqdm import tqdm

    _TQDM_AVAILABLE = True
except ImportError:
    _TQDM_AVAILABLE = False
# random.seed(1337)  # Set Seed for Program
import pandas as pd


def generate_item_tuple(
    pre_context, pre_target_context, target, post_target_context, post_context
):
    col_name = "Corr_token"

    try:
        if not pre_context.empty:
            pre_context_processed = TG.correct_punct(pre_context[col_name].values)

        elif pre_context.empty:
            pre_context_processed = ""
    except AttributeError:
        pre_context_processed = pre_context

    try:
        if not post_context.empty:
            post_context_processed = TG.correct_punct(post_context[col_name].values)

        elif post_context.empty:
            post_context_processed = ""
    except AttributeError:
        post_context_processed = post_context

    pre_target_context_processed = TG.correct_punct(pre_target_context[col_name].values)
    target_processed = TG.correct_punct(target[col_name].values)
    post_target_context_processed = TG.correct_punct(
        post_target_context[col_name].values
    )
    #
    # try:
    #     pre_context_processed
    # except NameError:
    #     pre_context_processed = pre_context
    #
    # try:
    #     post_context_processed
    # except NameError:
    #     post_context_processed = post_context

    return (
        pre_context_processed,
        pre_target_context_processed,
        target_processed,
        post_target_context_processed,
        post_context_processed,
    )


def generate_items_pandas(
    items,
    epoch_dict,
    window_size,
    num_items_e2=15,
    num_items_e4=15,
    num_items_e2_e4=30,
    max_len_sent_target=30,
    max_sampling_steps=10000,
):
    pos_tags_to_skip = ["$.", "$,", "$("]
    generated_items = {item: [] for item in items}
    # save already loaded dataframes here
    csv_loaded = dict()
    assert window_size % 2 == 0, "Please define an even window_size."
    index_before_after = int(window_size / 2)

    if _TQDM_AVAILABLE:
        items = tqdm(items)
    for item in items:
        generated_items_tmp = {key: [] for key in epoch_dict.keys()}
        print(f"Processing item '{item}'...")

        counter = 0
        while (
            len(generated_items_tmp["E2"]) != num_items_e2
            and len(generated_items_tmp["E4"]) != num_items_e4
            and len(generated_items_tmp["E2_E4"]) != num_items_e2_e4
        ) or counter <= max_sampling_steps:
            counter += 1
            epoch, csv_file_paths = random.choice(list(epoch_dict.items()))
            path_csv1, path_csv2 = random.choice(csv_file_paths)

            if path_csv1 not in csv_loaded:
                df1 = pd.read_csv(path_csv1, delimiter="\t", encoding="utf-8")
                csv_loaded[path_csv1] = df1
            else:
                df1 = csv_loaded[path_csv1]
            if path_csv2 not in csv_loaded:
                df2 = pd.read_csv(path_csv2, delimiter="\t", encoding="utf-8")
                csv_loaded[path_csv2] = df2
            else:
                df2 = csv_loaded[path_csv2]

            df1_only_rows_with_item = df1[df1["Corr_token"] == item]
            df2_only_rows_with_item = df2[df2["Corr_token"] == item]
            # TODO: add count for "skipping" punctuation for token count
            # generate sentence pairs + contexts
            if (
                len(df1_only_rows_with_item) > 0
                and len(df2_only_rows_with_item) > 0
            ):
                df1_only_rows_with_item = df1[df1["Corr_token"] == item].sample(1)
                df2_only_rows_with_item = df2[df2["Corr_token"] == item].sample(1)

                sent_id1 = df1_only_rows_with_item["Sent_ID"].values[0]
                sent_id2 = df2_only_rows_with_item["Sent_ID"].values[0]

                sent_len1 = len(df1[df1["Sent_ID"] == sent_id1])
                sent_len2 = len(df2[df2["Sent_ID"] == sent_id2])

                if sent_len1 <= max_len_sent_target and sent_len2 <= max_len_sent_target:

                    i1 = df1_only_rows_with_item.index.values[0]
                    i2 = df2_only_rows_with_item.index.values[0]
                    try:
                        target1 = df1.iloc[i1 : i1 + 1]
                        sent_id1 = target1["Sent_ID"].values[0]
                        target_sent1 = df1[df1["Sent_ID"] == sent_id1]
                        start_idx_target_sent1 = target_sent1.index[0]
                        end_idx_target_sent1 = target_sent1.index[-1]
                        target_before_sent1 = df1.iloc[start_idx_target_sent1:i1]
                        target_after_sent1 = df1.iloc[
                            i1 + 1 : end_idx_target_sent1 + 1
                        ]

                        num_tokens_before_rest1 = index_before_after - (
                            i1 - start_idx_target_sent1
                        )
                        num_tokens_after_rest1 = index_before_after - (
                            end_idx_target_sent1 - i1
                        )

                        context_after1 = ""
                        context_before1 = ""

                        # not enough pre-context available
                        # reason 1: target at beginning of document --> ad num_tokens_before_rest to post-context instead
                        if (
                            num_tokens_before_rest1 > 0
                            and (start_idx_target_sent1 - num_tokens_before_rest1)
                            <= 0
                        ):
                            context_before1 = ""  # df1[i+1:i+index_before_after+1]
                            context_after1 = df1[
                                end_idx_target_sent1
                                + 1 : end_idx_target_sent1
                                + index_before_after
                                + num_tokens_after_rest1
                                + num_tokens_before_rest1
                                + 1
                            ]
                        else:
                            context_before1 = df1[
                                start_idx_target_sent1
                                - num_tokens_before_rest1 : start_idx_target_sent1
                                # + 1
                            ]

                        try:
                            if context_after1.empty:
                                context_after1 = df1[
                                    end_idx_target_sent1
                                    + 1 : end_idx_target_sent1
                                    + num_tokens_after_rest1
                                    + 1
                                ]
                        except AttributeError:
                            context_after1 = df1[
                                end_idx_target_sent1
                                + 1 : end_idx_target_sent1
                                + num_tokens_after_rest1
                                + 1
                            ]

                        # not enough post-context available
                        # reason 1: target at end of document --> ad num_tokens_after_rest to pre-context instead
                        if (
                            num_tokens_after_rest1 > 0
                            and (end_idx_target_sent1 + num_tokens_after_rest1)
                            >= len(df1)
                            and context_after1.empty
                        ):
                            context_after1 = ""  # df1[i+1:i+index_before_after+1]
                            context_before1 = df1[
                                start_idx_target_sent1
                                - index_before_after
                                - num_tokens_after_rest1
                                - num_tokens_before_rest1 : start_idx_target_sent1  # +1
                            ]
                        # reason 2: post context longer than right side of context window
                        elif num_tokens_after_rest1 < 0 and context_after1.empty:
                            context_after1 = ""

                        target2 = df2.iloc[i2: i2 + 1]
                        sent_id2 = target2["Sent_ID"].values[0]
                        target_sent2 = df2[df2["Sent_ID"] == sent_id2]
                        start_idx_target_sent2 = target_sent2.index[0]
                        end_idx_target_sent2 = target_sent2.index[-1]
                        target_before_sent2 = df2.iloc[start_idx_target_sent2:i2]
                        target_after_sent2 = df2.iloc[
                                             i2 + 1: end_idx_target_sent2 + 1
                                             ]

                        num_tokens_before_rest2 = index_before_after - (
                                i2 - start_idx_target_sent2
                        )
                        num_tokens_after_rest2 = index_before_after - (
                                end_idx_target_sent2 - i2
                        )

                        context_after2 = ""
                        context_before2 = ""

                        # not enough pre-context available
                        # reason 1: target at beginning of document --> ad num_tokens_before_rest to post-context instead
                        if (
                                num_tokens_before_rest2 > 0
                                and (start_idx_target_sent2 - num_tokens_before_rest2)
                                <= 0
                        ):
                            context_before2 = ""  # df1[i+1:i+index_before_after+1]
                            context_after2 = df2[
                                             end_idx_target_sent2
                                             + 1: end_idx_target_sent2
                                                  + index_before_after
                                                  + num_tokens_after_rest2
                                                  + num_tokens_before_rest2
                                                  + 1
                                             ]
                        else:
                            context_before2 = df2[
                                              start_idx_target_sent2
                                              - num_tokens_before_rest2: start_idx_target_sent2
                                              # + 1
                                              ]

                        try:
                            if context_after2.empty:
                                context_after2 = df2[
                                                 end_idx_target_sent2
                                                 + 1: end_idx_target_sent2
                                                      + num_tokens_after_rest2
                                                      + 1
                                                 ]
                        except AttributeError:
                            context_after2 = df2[
                                             end_idx_target_sent2
                                             + 1: end_idx_target_sent2
                                                  + num_tokens_after_rest2
                                                  + 1
                                             ]

                        # not enough post-context available
                        # reason 1: target at end of document --> ad num_tokens_after_rest to pre-context instead
                        if (
                                num_tokens_after_rest2 > 0
                                and (end_idx_target_sent2 + num_tokens_after_rest2)
                                >= len(df2)
                                and context_after2.empty
                        ):
                            context_after2 = ""  # df1[i+1:i+index_before_after+1]
                            context_before2 = df2[
                                              start_idx_target_sent2
                                              - index_before_after
                                              - num_tokens_after_rest2
                                              - num_tokens_before_rest2: start_idx_target_sent2  # +1
                                              ]
                        # reason 2: post context longer than right side of context window

                        elif num_tokens_after_rest2 < 0 and context_after2.empty:
                            context_after2 = ""

                        item1 = (
                            context_before1,
                            target_before_sent1,
                            target1,
                            target_after_sent1,
                            context_after1,
                        )
                        item1 = generate_item_tuple(*item1)

                        # add meta info
                        item1_final = (item1, [path_csv1, item, sent_id1, epoch])
                        item2 = (
                            context_before2,
                            target_before_sent2,
                            target2,
                            target_after_sent2,
                            context_after2,
                        )
                        item2 = generate_item_tuple(*item2)

                        # add meta info
                        item2_final = (item2, [path_csv2, item, sent_id2, epoch])

                        if (item1_final, item2_final) not in generated_items_tmp[epoch]:

                            if epoch == "E2":
                                if len(generated_items_tmp[epoch]) < num_items_e2:
                                    generated_items_tmp[epoch].append((item1_final, item2_final))
                                    print(
                                        f"Unique item found in {path_csv2}, adding to list..."
                                    )

                            elif epoch == "E4":
                                if len(generated_items_tmp[epoch]) < num_items_e4:
                                    generated_items_tmp[epoch].append((item1_final, item2_final))
                                    print(
                                        f"Unique item found in {path_csv2}, adding to list..."
                                    )

                            elif epoch == "E2_E4":
                                if len(generated_items_tmp[epoch]) < num_items_e2_e4:
                                    generated_items_tmp[epoch].append((item1_final, item2_final))
                                    print(
                                        f"Unique item found in {path_csv2}, adding to list..."
                                    )

                        else:
                            pass
                            # print("Item already in list, skipping...")

                    except Exception as e:
                        print(
                            f"An error occurred in row with indices {i1, i2}, skipping..."
                        )
                        if _PYTHON_VERSION[1] <= 8:
                            print(e)
                        else:
                            traceback.print_exception(e)

            if len(generated_items_tmp["E2"]) == num_items_e2 and len(generated_items_tmp["E4"]) == num_items_e4 and len(generated_items_tmp["E2_E4"]) == num_items_e2_e4:
                counter += max_sampling_steps

        e2_items_tmp_values = generated_items_tmp["E2"]
        e4_items_tmp_values = generated_items_tmp["E4"]
        e2_e4_items_tmp_values = generated_items_tmp["E2_E4"]

        if (
            len(e2_items_tmp_values) >= num_items_e2
            and len(e4_items_tmp_values) >= num_items_e4
            and len(e2_e4_items_tmp_values) >= num_items_e2_e4
        ):
            generated_items[item] += e2_items_tmp_values
            generated_items[item] += e4_items_tmp_values
            generated_items[item] += e2_e4_items_tmp_values
            random.shuffle(generated_items[item])

        else:
            print("Not enough items found in at least one epoch, skipping item...")

    # process final item dict in parallel and write n item pairs sequentially to list, such that result list has format:
    # [item_1_1, item_2_1,... item_n_1, ... item_1_2, item2_2, .. item_n_2, ...]
    zip_list_values = list(zip(*generated_items.values()))

    results_flattened = []
    for item in zip_list_values:
        for item_pair in item:
            results_flattened.append(item_pair)

    return results_flattened


def all_unique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)


def get_targets(filename, target, window_size):
    # basically runscript() des sub-programms

    csv_list, results = TG.get_data(filename, target)
    line_number = TG.get_list_number(csv_list, results)

    (
        target_word_list,
        window_before,
        window_after,
        target_sid_list,
        window_before_sid,
        window_after_sid,
    ) = TG.get_window(line_number, csv_list, window_size)
    targets, targets_sid_list = TG.get_sent(
        target_word_list,
        window_before,
        window_after,
        target_sid_list,
        window_before_sid,
        window_after_sid,
    )
    targets_final, targets_final_sid = TG.filter_target(targets, targets_sid_list)

    ##Erstellung der Zufallsvariable
    ##Wenn es kein Vorkommen des Targetworts gibt Return False
    if len(targets_final) == 0:
        return False
    ##Wenn es nur ein Vorkommen gibt dann Zufallsvariable 0 zum Indexen von Position 0
    ##Und Funktion laufen lassen.
    elif len(targets_final) == 1:
        rand_numb = 0
        (
            target_context_before,
            target_sent_before,
            target_word,
            target_sent_after,
            target_context_after,
            target_random_sid,
        ) = TG.get_random(targets_final, rand_numb, targets_final_sid)
    ##In allen "normalen" Faellen eine Zufallsvariable erstellen und FUnktion laufen lassen
    else:
        rand_numb = random.randint(0, len(targets_final) - 1)
        (
            target_context_before,
            target_sent_before,
            target_word,
            target_sent_after,
            target_context_after,
            target_random_sid,
        ) = TG.get_random(targets_final, rand_numb, targets_final_sid)

    ##Log-Info List mit Corpusname, Targetwort, und die SID des Target words.
    log_data = []
    log_data.append(filename)
    log_data.append(target)
    log_data.append(target_random_sid)

    output_tuple = (
        target_context_before,
        target_sent_before,
        target_word,
        target_sent_after,
        target_context_after,
    )

    output_tuple = TG.string_process(output_tuple)

    return output_tuple, log_data


def generate_items(
    target_list,
    epochen_dict,
    window_size,
    minquant_e2=15,
    minquant_e4=15,
    minquant_e2_e4=30,
):
    """
    Input:
    target_list(list) - Liste an Target Wörtern (strings), die gesucht werden sollen
    epochen_dict(dict) - Dictionary mit den Epochen, Key sind die Kennungen "E2", "E4", "E2E4", Values sind jeweils listen an Tuplen, jeder Eintrag des Tuples ist ein Dateiname
    window_size(int) - Window Size des Output (Tokens vor und nach dem Satz, in dem das Target Word vorkommt)

    Output:
    results_list(list) - Liste mit Tuplen, immer 2 Items pro Tuple. Jedes Item ist selber ein Tuple, 0 ist der Satz, aufgeteilt in 5 strings, 1 sind die Log-Daten

    Das Programm Iteriert durch alle Targets, darin durch die Epochen-Kennungen und darin durch die Liste pro Epoche.

    Jede Epoche hat einen minquant (minimum quantity) wert. Für E2 und E4 sind es jeweils 15, für E2E4 sind es 30
    Findet das Programm  genug (15 bzw. 30) Items, macht es automatisch weiter.
    Jedes Target hat also 60 Items

    final_results_list(list) ist am Ende noch der Reihenfolge nach und muss geshuffled werden (mit seed)
    """

    debugmode = True
    epochen_key_list = ["E2", "E4", "E2_E4"]
    minquant_dict = {"E2": minquant_e2, "E4": minquant_e4, "E2_E4": minquant_e2_e4}

    final_results_list = (
        []
    )  # Liste mit Items und Log Dateien, angelegt in Tupeln, ein Tuple ist immer ein Item, welches aus 2 Sätzen besteht
    loopmustbreak = False

    # Iterieren durch alle Targets
    if _TQDM_AVAILABLE:
        target_list = tqdm(target_list)
    for target in target_list:
        results_list = []  # Liste zum zwischenspeichern aller Items für ein Target
        logdata_checklist = (
            []
        )  # Liste um Logdaten zwischenzuspeichern und zu überprüfen, ob ein Item schon einmal vorkam

        if debugmode == True:
            print("####### " + "processing " + target + " #######\n")

        # Iteriert durch die Keys des Epochen Dict.
        for epoche in epochen_key_list:
            if debugmode == True:
                print("####### " + "processing in " + epoche + " #######\n")

            minquant_counter = 0

            # Interiert durch die Liste an Tuplen, die einer jeden Epoche hinterlegt ist
            for corpus_tuple in epochen_dict[epoche]:
                if minquant_counter < minquant_dict[epoche]:
                    results = ()

                    # Iteriert durch das Tuple
                    for text in corpus_tuple:
                        # Notfall Break (?)
                        if loopmustbreak == True:
                            loopmustbreak = False
                            break

                        if debugmode == True:
                            print("processing " + target + " in " + text)

                        # Reset der Test-Variable
                        tuple_unique = False

                        # Generiert eins von 2 Ergebnissen, wiederholt für das Zweite
                        while tuple_unique == False:
                            # Target wird generiert und zwischengespeichert
                            result = get_targets(text, target, window_size)

                            # wenn das Wort nicht im Text gefunden wird, verwerfen
                            if result == False:
                                loopmustbreak = True

                                if debugmode == True:
                                    print(target + " not in Text, break \n")

                                break

                            result[1].append(epoche)  # epoche in die log datei

                            # Wenn das Ergebnis noch nicht zuvor vorkam, abspeichern
                            # Wenn doppelt, abbrechen.

                            if result[1] not in logdata_checklist:
                                if debugmode == True:
                                    print("saving to results tuple")

                                # Log-Data für Duplikationscheck abspeichern
                                logdata_checklist.append(result[1])

                                results += (result,)
                                tuple_unique = True

                            else:
                                if debugmode == True:
                                    print("item doubled, break \n")
                                results = ()
                                break

                    if results:
                        if debugmode == True:
                            print("saving to results_list")
                        results_list.append(results)
                        minquant_counter += 1
                        if debugmode == True:
                            print(
                                "Counter: "
                                + str(minquant_counter)
                                + " out of "
                                + str(minquant_dict[epoche])
                                + " for "
                                + epoche
                                + "\n"
                            )

        # Check, ob alle gefundenen Items unique sind, aka: keine Dopplungen
        if all_unique(logdata_checklist):
            if debugmode == True:
                print("all Items unique")
        # Check, ob genug Items für ein Target Wort gefunden wurden. Wenn nicht, verwerfen
        if (
            len(results_list)
            == minquant_dict["E2"] + minquant_dict["E4"] + minquant_dict["E2_E4"]
        ):
            if debugmode == True:
                print("enough Items found for " + target + ", saving to final list\n")
            for i in results_list:
                final_results_list.append(i)
        else:
            if debugmode == True:
                print(
                    "not enough Items for " + target + " found, moving to next target\n"
                )

    # shufflen der liste
    random.shuffle(final_results_list)

    return final_results_list


def main():
    ex_filename = "data/test/annotations/weigel_gnothi_1615.csv"
    ex_filename2 = "data/test/annotations/dannhauer_catechismus04_1653.csv"

    ex_epochen_dict = {
        "E2": [
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
        ],
        "E4": [
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
        ],
        "E2_E4": [
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
            (ex_filename, ex_filename),
            (ex_filename, ex_filename2),
            (ex_filename2, ex_filename2),
        ],
    }

    ex_target_list = ["Gott", "Sonne"]

    window_size = 50

    final_targets = generate_items(
        ex_target_list, ex_epochen_dict, window_size, 2, 2, 2
    )

    for i in final_targets:
        print(i)
    print(len(final_targets))
    return final_targets


debugmode = False

if __name__ == "__main__":
    # debugmode = True
    # final_targets = main()

    import pickle

    items = ["und", "aber", "er", "sie", "es"]
    path_docs_pairwise = "data/test/docs_pairwise/docs_pairwise.pkl"
    with open(path_docs_pairwise, "rb") as f:
        doc_pairwise = pickle.load(f)
    import os

    for k, v in doc_pairwise.items():
        for i, l in enumerate(v):
            doc_pairwise[k][i][0] = os.path.join(
                "data/test/annotations/", doc_pairwise[k][i][0] + ".csv"
            )
            doc_pairwise[k][i][1] = os.path.join(
                "data/test/annotations/", doc_pairwise[k][i][1] + ".csv"
            )

    # doc_pairwise["E2"] = [doc_pairwise["E2"][0]]
    # doc_pairwise["E4"] = [doc_pairwise["E4"][0]]
    # doc_pairwise["E2_E4"] = [doc_pairwise["E2_E4"][0]]

    out = generate_items_pandas(items, doc_pairwise, 80, 5, 5, 10, 50, 100)
