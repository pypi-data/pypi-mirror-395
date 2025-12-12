from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA
from fuzzic.configuration.config import config

def interpretability(rulebase):
    '''
    If the number of variables is less than the interpretabiliy threshold number (see config), interpretability is 100%
    If not, it is interpretabiliy threshold number / number of variables
    '''
    nb_variables = len(rulebase.var)
    threshold = config.interpretability_threshold_number

    if nb_variables <= threshold:
        score = 1
    else:
        score = threshold/nb_variables
    dico = {"warning" : "", "score" : score}
    return dico

CRITERIA.append(criterion(name="number of variables", category="fuzzy rule base",
          active=True, func_interpretability=interpretability))
