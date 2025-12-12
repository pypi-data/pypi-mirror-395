CRITERIA = [] # The list of interpretability criterion instances

class criterion:
    def __init__(self, name, category="", 
                 direction="", 
                 active=False, 
                 func_interpretability=None, 
                 weight = 1):
        # my_path = importlib.import_module(path + name, package=None)
        # my_path = importlib.import_module(".".join(__name__.split('.')[:-1]+['criteria', name]), package=None)
        self.category = category
        self.criterion_name = name
        self.active = active
        self.weight = weight
        self.interpretability = func_interpretability

    def __str__(self):
        return (f'[{self.criterion_name}]: {{' +
                ', '.join((f'{name}: {self.__getattribute__(name)}' for name in self.__dict__ if 'name' not in name)) +
                '}')
                
    def __repr__(self):
        return str(self)
    

def status():
    criteria = sorted([(_.criterion_name, _.active) for _ in CRITERIA])
    return '\n'.join(f'{c_name}: {"in" if not c_active else ""}active' for c_name, c_active in criteria)

def __onoff__(criterion_name, active):
    for _ in CRITERIA:
        if _.criterion_name.lower() == criterion_name.lower():
            _.active = active
            break
    else:
        print("Unknown criterion")
        
def update_sugeno_weight(criterion_name, weight):
    for _ in CRITERIA:
        if _.criterion_name.lower() == criterion_name.lower():
            _.sugeno_weight = weight
            break
    else:
        print("Unknown criterion")

def activate(criterion_name):
    """
    Change the status of the criterion <criterion_name> to 'evaluable'.
    If <criterion_name> is a collection, the status is changed to 'evaluable' on each element.

    :param criterion_name: the name or the collection of names of criterion to activate
    """
    if criterion_name == "all":
        for c in CRITERIA:
            __onoff__(c.criterion_name, active = True)
    elif isinstance(criterion_name, (list, tuple, set)):
        for c in criterion_name: __onoff__(c, active=True)
    else:
        __onoff__(criterion_name, active=True)

def deactivate(criterion_name):
    """
    Change the status of the criterion <criterion_name> to 'not evaluable'.
    If <criterion_name> is a collection, the status is changed to 'not evaluable' on each element.

    :param criterion_name: the name or the collection of names of criterion to deactivate
    """
    if criterion_name == "all":
        for c in CRITERIA:
            __onoff__(c.criterion_name, active = False)
    elif isinstance(criterion_name, (list, tuple, set)):
        for c in criterion_name: __onoff__(c, active=False)
    else:
        __onoff__(criterion_name, active=False)

def evaluate_interpretability(study, particular_rulebase = None):
    '''
    input : the file path to the rulebase you want to analyse
    output : a result file in json format in results folder
    '''
    all_results = dict()
    for rulebase in study.rulebases:
        interpretability_result = evaluate_interpretability_rulebase(rulebase)
        all_results[rulebase.filename] = interpretability_result
    return all_results

def evaluate_interpretability_rulebase(rulebase):
    '''
    input : a rulebase object
    output : the dictionnary of interpretability scores
    '''

    interpretability_result = dict()
    for C in (c for c in CRITERIA if c.active):
        print(f'Evaluate criteria [{C.criterion_name}]', end=' ')
        result = C.interpretability(rulebase)
        print(result)
        interpretability_result[C.criterion_name] = result
    return interpretability_result


# Do not remove. Necessary to initiate already defined criteria.
import fuzzic.interpretability.criteria





















