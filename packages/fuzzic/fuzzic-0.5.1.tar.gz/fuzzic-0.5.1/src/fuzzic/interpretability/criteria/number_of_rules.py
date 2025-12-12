from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA
from fuzzic.configuration.config import config

def interpretability(rulebase):
    '''
    If the number of rules is less than the interpretabiliy threshold number (see config), then its interpretability is 100%
    If not, its interpretabiliy is threshold number / nb of rules
    '''
    nb_rules = len(rulebase.rules)
    threshold = config.interpretability_threshold_number
    if nb_rules <= threshold:
        res = 1
    else:
        res = threshold/nb_rules
    dico = {"warning" : "", "score" : res}
    return dico

CRITERIA.append(criterion(name="number of rules", category="fuzzy rule base",
          active=True, func_interpretability=interpretability))
