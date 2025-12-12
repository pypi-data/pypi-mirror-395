import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA
from fuzzic.configuration.config import config

def interpretability(rulebase):
    '''
    If the size of the rule is less than the interpretabiliy threshold number (see config), then the rule contributes to interpretability with 100%
    If not, its contribution is interpretabiliy threshold number / length
    '''
    rules = rulebase.rules
    collection = []
    threshold = config.interpretability_threshold_number
    for key in rules.keys():
        length = len(rules[key].premisse) + len(rules[key].conclusion)
        if length <= threshold:
            collection.append(1)
        else:
            collection.append(threshold/length)
    
    result = fuzzy_logic_manager.criteria_aggregator(collection = collection)
    dico = {"warning" : "", "score" : result}
    return dico

CRITERIA.append(criterion(name="rule size", category="fuzzy rule",
          active=True, func_interpretability=interpretability))

