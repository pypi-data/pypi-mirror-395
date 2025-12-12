import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
from fuzzic.configuration.config import config
from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA
import numpy as np

def interpretability(rulebase):
    '''
    Discretise the universe of all variables and establish for each input if
    complementarity is filled. 
    Collection contains all such inputs.
    '''
    all_var = rulebase.used_variables
    war = ""
    all_results = []
    for key in all_var.keys():
        var = all_var[key]
        Tv = var.all_sef
        respect_of_complementarity = []
        for x in var.espace:
            somme = 0
            for S in Tv:
                somme += S.forward(x)
            somme = fuzzy_logic_manager.rounding(somme)
            if abs(somme - 1) > config.precision:
                respect_of_complementarity.append(0)
                if war == "":
                    war += "Complementarity not filled for variable \"" + str(var.label) + "\" with input : " + str(round(x, 2)) + ", the sum of membership values is: " + str(round(somme, 2))
            else:
                respect_of_complementarity.append(1)
        percentage_complementarity = np.mean(respect_of_complementarity)
        all_results.append(percentage_complementarity)

    print("\n\nall_results", all_results, "\n\n")
    result = fuzzy_logic_manager.criteria_aggregator(collection = all_results)
    score = fuzzy_logic_manager.rounding(result)
    dico = {"warning" : war, "score" : score}
    return dico

CRITERIA.append(criterion(name="complementarity", category="linguistic variables", 
          active=True, func_interpretability=interpretability))
