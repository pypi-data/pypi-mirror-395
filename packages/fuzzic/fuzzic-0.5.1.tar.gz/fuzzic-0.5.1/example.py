from fuzzic.study.study import Study, create_project
from fuzzic.interpretability.interpretability_manager import CRITERIA, criterion, status, deactivate, activate, update_sugeno_weight
from fuzzic.configuration.config import config

study_name = "climatiseur" # the folder name in working_dir/study where the rule-base and all the results are/will be stored

S = Study(study_name)

# IF YOU WANT TO ACTIVATE ONLY SOME CRITERIA:    
deactivate("all")
activate("consistency")
activate("justifiable number of elements")
activate("normality")
activate("complementarity")
activate("uniformity")
activate("coverage")


S.evaluate()

S.generate_dashboard()

