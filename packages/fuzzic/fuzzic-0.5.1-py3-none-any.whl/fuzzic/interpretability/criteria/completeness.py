import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA

def interpretability(rulebase):
    '''
    Compute the percentage of active data in the dataset
    '''
    dataset = rulebase.get_dataset()
    nb_data_actifs = 0
    war = ""
    
    for i in range(len(dataset.data)):
        input_activated = False
        for key in rulebase.rules.keys():
            rule = rulebase.rules[key]
            activation = fuzzy_logic_manager.check_activation(rule, dataset.labels, dataset.data[i])
            if activation:
                nb_data_actifs += 1
                input_activated = True
                break
        if not input_activated and war == "":
            war += "The input data: "
            j = 0
            for key in rulebase.var.keys():
                war += "\"" + rulebase.var[key].label + "\": " + str(round(float(dataset.data[i][j]), 2)) + ", "
                j +=1
            war += " is not activated in the rulebase."
    score = fuzzy_logic_manager.rounding(nb_data_actifs / len(dataset.data))
    dico = {"warning" : war, "score" : score}
    return dico

CRITERIA.append(criterion(name="completeness", category="fuzzy rule base", 
          active=True, func_interpretability=interpretability))
