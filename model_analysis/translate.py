import locale
import pylcs
import numpy as np
# locale.setlocale(locale.LC_ALL, "")

def translate_label(label):
    return (
        label
        .replace("Comparing COVID-19 reported, modeled and predicted deaths\nfor ",
                "Comparaison des décès et cas de COVID19 officiels, modélisés et prédits\nen ")
        .replace("Plots of daily fatalities", "Courbes des décès journaliers")
        .replace("Plots of cumulated fatalities", "Courbes du cumul des décès")
        .replace("Progression of the epidemic:\n reproduction number and infections",
                 "Progression de l'épidémie :\n taux de reproduction et infections")
        .replace("Reported deaths ", "Décès officiels ")
        .replace("Reported cases ", "Cas confirmés ")
        .replace("Social distancing", "Distanciation sociale")
        .replace("forecast from", "Prédiction depuis")
        .replace("model ", "Modèle ")
        .replace("Lockdown", "Confinement")
        .replace("Cancel events", "Evenements annulés")
        .replace("School closures", "Fermeture des écoles")
        .replace("Self-isolation\nwhen ill", "Quarantaine")
        .replace("Daily deaths", "Décès journaliers")
        .replace("Total deaths", "Décès cumulés")
        .replace("Daily new cases", "Infections journalières")
        .replace("log scale", "log")
        .replace("1000s", "x1000")
        .replace(" to ", " au ")
        .replace(" and ", " et ")
    )

def translate_legend(ax):
    leg = ax.get_legend()
    if hasattr(leg, "get_texts"):
        for label in leg.get_texts():
            label.set_text(
                translate_label(label.get_text())
            )

def translate_axis_labels(ax):
    locale.setlocale(locale.LC_TIME, "fr_FR")
    ax.set_ylabel(translate_label(ax.get_ylabel()))
    ax.set_xlabel(translate_label(ax.get_xlabel()))
    ax.set_title(translate_label(ax.get_title()))

def translate_axes_to_french(axs):
    if type(axs) != type(list()):
        axs = [axs]
    for ax in axs:
        translate_legend(ax)
        translate_axis_labels(ax)
    for child in axs[0].figure.get_children():
        if hasattr(child, "set_text") and hasattr(child, "get_text"):
            child.set_text(translate_label(child.get_text()))

def  most_probable_match(string, possible_strings, n_matches=1):
    """ Fuzzy lookup for a similar string
    """

    def return_match(arg_most_prob, probable_match, i_match=1):
        print(
            f"\tMatch {i_match} of {n_matches} : "
            + f"'{possible_strings[arg_most_prob]}' == '{string}'  "
            + f"with a match score of {probable_match[arg_most_prob]}/{4*len(string)}."
        )
        return possible_strings[arg_most_prob]

    possible_strings_l = [s.lower() for s in possible_strings]
    string_l = string.lower()
    lcsubsequence_list_lower = pylcs.lcs_of_list(string_l, possible_strings_l)
    probable_match = (np.add(np.add(
        pylcs.lcs_of_list(string, possible_strings),  # longest subsequence 
        pylcs.lcs2_of_list(string, possible_strings) # longest substring
    ), np.add(
        lcsubsequence_list_lower,  # longest subsequence case insensitive
        pylcs.lcs2_of_list(string_l, possible_strings_l) # longest substring case insensitive
    )).astype(np.int) - (
        np.array([2*(len(t) - m) for t, m in zip(possible_strings_l, lcsubsequence_list_lower)])  # Penalise extra characters in the match
    ))
    if n_matches == 1:
        arg_most_prob = np.argmax(probable_match)
        return return_match(arg_most_prob, probable_match)
    elif n_matches > 1:
        args_most_prob = np.argpartition(probable_match, -n_matches)[-1:-n_matches-1:-1]
        return [return_match(a, probable_match, i+1) for i, a in enumerate(args_most_prob)]
    else: 
        raise AttributeError("Invalid number of matches requested")
