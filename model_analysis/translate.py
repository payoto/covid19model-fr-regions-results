import locale
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