import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
from fuzzic.interpretability.interpretability_manager import criterion, CRITERIA

def interpretability(rulebase):
    '''
    If 2 premisse gives different conclusions, compute the similarity between the conclusions (must be maximised for consistency)
    '''
    
    def check_two_premisses(pre1, pre2):
        representation1 = hash(repr({t.sef.var.label + t.sef.label for t in pre1}))
        representation2 = hash(repr({t.sef.var.label + t.sef.label for t in pre2}))
        return representation1 == representation2
    
    def check_same_premisse_give_same_conclusion(rules):
        all_results = []
        war = ""
        for i in range(len(rules)-1):
            for j in range(i+1, len(rules)):
                if check_two_premisses(rules[i].premisse, rules[j].premisse):
                    for t1 in rules[i].conclusion:
                        for t2 in rules[j].conclusion:
                            if t1.var.ident == t2.var.ident and t1.sef.ident != t2.sef.ident:
                                sim = fuzzy_logic_manager.similarity(t1, t2)
                                all_results.append(sim)
                                if sim < 1 and war == "":
                                    war = "Rule \"" + rules[i].ident + "\" and \"" + rules[j].ident + "\" are unconsistents. (For conclusion variable \"" + t1.sef.var.label + "\", fuzzy sets: \"" + t1.sef.label + "\" and \"" + t2.sef.label + "\"have a similarity of " + str(round(sim, 2)) + ")"
        
        if len(all_results) == 0:
            all_results = [1]
        #print("all_results",all_results)
        return all_results, war
            
    rules = [rulebase.rules[key] for key in rulebase.rules.keys()]
    all_results, war = check_same_premisse_give_same_conclusion(rules)
    score = fuzzy_logic_manager.criteria_aggregator(collection = all_results)
    dico = {"warning" : war, "score" : fuzzy_logic_manager.rounding(score)}
    return dico

CRITERIA.append(criterion(name="consistency", category="fuzzy rule base", 
          active=True, func_interpretability=interpretability))
