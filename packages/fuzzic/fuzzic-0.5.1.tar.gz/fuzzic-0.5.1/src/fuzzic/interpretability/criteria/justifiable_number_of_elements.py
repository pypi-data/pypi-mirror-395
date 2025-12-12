import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA
from fuzzic.configuration.config import config


def interpretability(rulebase):
    '''
    If a number of element for a variable is less than the interpretabiliy threshold number (see config), then it contributes to interpretability with 100%
    If not, its contribution is interpretabiliy threshold number / size of partition
    '''
    all_results = []
    threshold = config.interpretability_threshold_number
    for key in rulebase.var.keys():
        var = rulebase.var[key]
        Tv = var.all_sef
        taille = len(Tv)
        assert taille > 0, "Variable" + str(var.label) + "has no fuzzy set"
        if taille <= threshold:
            all_results.append(1)
        else:
            all_results.append(threshold/taille)
    result = fuzzy_logic_manager.criteria_aggregator(collection = all_results)
    dico = {"warning" : "", "score" : fuzzy_logic_manager.rounding(result)}
    return dico
CRITERIA.append(criterion(name="justifiable number of elements", category="linguistic variables", 
          active=True, func_interpretability=interpretability))
