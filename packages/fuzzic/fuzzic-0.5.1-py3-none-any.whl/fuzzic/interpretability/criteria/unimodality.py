import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA

def interpretability(rulebase):
    '''
    Computes the proportion of unimodal fuzzy sets.
    '''
    all_sef = rulebase.get_all_sef()
    total = len(all_sef)
    compteur = len(all_sef)
    war = ""
    for sef in all_sef:
        if sef.shape not in ["gaussian", "triangle", "one_point"] or sef.hauteur_y != 1:
            compteur = compteur - 1
            if war == "":
                war = "Fuzzy set: \"" + sef.label + "\" from variable: \"" + sef.var.label + "\" is not unimodal."
    dico = {"warning" : war, "score" : fuzzy_logic_manager.rounding(compteur / total)}
    return dico

CRITERIA.append(criterion(name="unimodality", category="fuzzy sets",
          active=True, func_interpretability=interpretability))
