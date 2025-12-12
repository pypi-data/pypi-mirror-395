import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA
from fuzzic.configuration.config import config

def interpretability(rulebase):
    '''
    For each input of the dataset, computes the number of activated rules in the same time.
    If such number is below the inetrpretability threshold number (see Config), then the contribution for interpretability is 1.
    If not, then its contribution is threshold / nb_rules_activated
    '''
    dataset = rulebase.get_dataset()
    threshold = config.interpretability_threshold_number

    collection_of_activations = []
    for i in range (len(dataset.data)):
        nb_rules_activated = 0
        for key in rulebase.rules.keys():
            rule = rulebase.rules[key]
            activation = fuzzy_logic_manager.check_activation(rule, dataset.labels, dataset.data[i])
            if activation:
                nb_rules_activated += 1
        if nb_rules_activated <= threshold:
            collection_of_activations.append(1)
        else:
            collection_of_activations.append(threshold / nb_rules_activated)

    result = fuzzy_logic_manager.criteria_aggregator(collection = collection_of_activations)
    score = fuzzy_logic_manager.rounding(result)
    dico = {"warning" : "", "score" : score}
    return dico

CRITERIA.append(criterion(name="number rules activated", category="fuzzy rule base",
          active=True, func_interpretability=interpretability))
