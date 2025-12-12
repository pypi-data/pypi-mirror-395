import os
import json
import datetime
import fuzzic.interpretability.interpretability_manager as interpretability_manager
from fuzzic.configuration.config import config
import fuzzic.interpretability.fuzzy_logic_manager as fuzzy_logic_manager
import fuzzic.data_management.import_manager as import_manager
from fuzzic.interpretability.interpretability_manager import CRITERIA
from fuzzic.visualization.dashboard import get_dashboard

study_path = os.path.realpath(os.getcwd())

def create_project(study_name = "Study", study_root="study", path = None):
    """
   Create the project folder in the study directory.

   Parameters
   ----------
   study_name : str
       name of the study
   study_root : str
       folder in which the study and the results will remain

   Returns
   -------
   Nothing
   """
    if path is None:
        study_directory = os.path.join(study_path, study_root, study_name)
        if os.path.isdir(study_directory):
            time = datetime.datetime.today().strftime('%Y-%m-%d--%H:%M:%S')
            ref_study = study_name + "_" + time
            print("Study name already exist, it now refers to :" + ref_study) 
            study_directory = os.path.join(path, study_root, ref_study)
            
        else:
            ref_study = study_name
        os.mkdir(study_directory)
    else:
        study_directory = path
        ref_study = study_name
    
    #print("STUDY DIRECTORY IS :", study_directory)
    
    dataset_directory = os.path.join(study_directory, "datasets")
    if not os.path.isdir(dataset_directory):
        os.mkdir(dataset_directory)
    
    rulebase_directory = os.path.join(study_directory, "rulebases")
    if not os.path.isdir(rulebase_directory):
        os.mkdir(rulebase_directory)
    
    results_directory = os.path.join(study_directory, "results")
    if not os.path.isdir(results_directory):
        os.mkdir(results_directory)
    
    specifics_directory = os.path.join(study_directory, "specifics")
    if not os.path.isdir(specifics_directory):
        os.mkdir(specifics_directory)
    
    dashboard_directory = os.path.join(study_directory, "dashboard")
    if not os.path.isdir(dashboard_directory):
        os.mkdir(dashboard_directory)
    
    print("Study is ready to set! Reference: " + ref_study)
    print("\nPlease drop at least one rulebase in the rulebases folder before creating object Study.")


def load_study(ref_study):
    """
   load the study object from the reference

   Parameters
   ----------
   ref_study : str
       reference of the study
   
   Returns
   -------
   Nothing
   """
   
    return Study(ref_study, True)

class Study:
    def __init__(self, ref_study = "Study", ref_study_root="study", already_set = False, path = None):
        self.ref_study = ref_study
        self.criteria = CRITERIA
        
        if path is None:
            self.study_directory = os.path.join(study_path, ref_study_root, ref_study)
        else:
            self.study_directory = path
        self.rulebases_directory = os.path.join(self.study_directory, "rulebases")

        self.dataset = None
        self.rulebases = None
        self.first_rulebase = None

        self.import_rulebases()
        self.create_dataset()
        
        if not already_set:
            #self.dump_dataset()
            self.initiate_specifics()
    
    def __repr__(self):
        return "study_" + str(self.ref_study)
        
    def initiate_specifics(self):
        """
       Initialize the study with specific files that are needed for some criteria
       """        
        specifics_directory = os.path.join(self.study_directory, "specifics")
        
        dico_prototype = dict()
        dico_label_order = dict()
        
        variables = self.rulebases[0].var
        
        for key in variables.keys():
            dico_label_order[key] = dict()
            for s in variables[key].all_sef:
                dico_label_order[key][s.label] = 0
        label_orders = os.path.join(specifics_directory, "label_orders.json")
        with open(label_orders, 'w') as f:
            json.dump(dico_label_order, f, sort_keys=True, indent=4, separators=(',', ': '))
        
        for key in variables.keys():
            dico_prototype[key] = []
            
        prototypes_file = os.path.join(specifics_directory, "prototypes.json")
        with open(prototypes_file, 'w') as f:
            json.dump(dico_prototype, f, sort_keys=True, indent=4, separators=(',', ': '))
        
        similar_var_file = os.path.join(specifics_directory, "similar_variables.dat")
        with open(similar_var_file, 'w') as f:
            pass

    
    def create_dataset(self):
        one_rulebase = self.rulebases[0]
        data = one_rulebase.create_dataset()
        self.dataset = data
        dataset_path = os.path.join(self.study_directory, "datasets")
        dataset_file = os.path.join(dataset_path, "one_dataset.data")
        with open(dataset_file, "w") as g:
            for j in range(len(data.labels)):
                lab = data.labels[j]
                g.write(str(lab))
                if j < len(data.labels) - 1:
                    g.write(",")
            g.write("\n")
            for one_data in data.data:
                for i in range(len(one_data)):
                    one_value = one_data[i]
                    g.write(str(one_value))
                    if i < len(one_data)-1:
                        g.write(",")
                g.write("\n")
                
    
    def import_rulebases(self, particular_rulebase_name = None):
        #getting all rulebases in the rulebase folder of the study
        if particular_rulebase_name is None:
            all_rulebases_names = os.listdir(self.rulebases_directory)
            all_rulebases = [os.path.join(self.rulebases_directory, rb) for rb in all_rulebases_names if not rb.endswith('.gitkeep')]
            self.rulebases = [import_manager.import_rulebase(rb) for rb in all_rulebases]
        else:
            rb = os.path.join(self.rulebases_directory, particular_rulebase_name)
            self.rulebases = [import_manager.import_rulebase(rb)]
        for rb in self.rulebases:
            rb.study = self
            rb.dataset = self.dataset
        self.first_rulebase = self.rulebases[0]
    
    
    def save_results(self, rulebase_name, results):
        result_path = os.path.join(self.study_directory, "results")
        file_path = os.path.join(result_path, rulebase_name + ".json")
        with open(file_path, "w") as f:
            json.dump(results, f, sort_keys=True, indent=4, separators=(',', ': '))

#GESTION DES POIDS POUR LINTEGRALE DE SUGENO A FAIRE
    
    def get_results(self, particular_rulebase_name = None):
        results = interpretability_manager.evaluate_interpretability(self, particular_rulebase_name)
        new_results = dict()
        col1_width = 30
        col2_width = 20
        print("\n====\n")
        print(f"{'Rulebase':<{col1_width}}{'Interpretability':<{col2_width}}")

        for key in results.keys():
            res = results[key]
            if config.criteria_pooling != "none":
                pooling = fuzzy_logic_manager.score_pooling(res)
                res["total"] = dict()
                res["total"]["score"] = pooling
                res["total"]["type"] = config.criteria_pooling
                #print(f"{key:<{col1_width}}{round(pooling*100,2):<{col2_width}}")
                print(f"{key:<{col1_width}}{(str(round(pooling*100, 2)) + ' %'):<{col2_width}}")
                #print("\n====================\nFor rulebase: " + str(key) + ", global interpretability is: " + str(round(pooling*100,2)) + "%.\n====================\n")
            new_results[key] = res
        print("\n====\n")
        return new_results
    
    def evaluate(self, particular_rulebase_name = None):
        interpretability_result = self.get_results(particular_rulebase_name)
        for rulebase in self.rulebases:
            rulebase.interpretability = interpretability_result[rulebase.filename]
            if rulebase.filename is not None:
                self.save_results(os.path.splitext(rulebase.filename)[0], rulebase.interpretability)
        print("Evaluation of interpretability of rule bases of : " + self.ref_study + " successful !\n")
        result_path = os.path.join(self.study_directory, "results")
        print("Results of evaluation available in " + result_path)
    
    def generate_dashboard(self, output_file="dashboard.html"):
        html_content = get_dashboard(self.rulebases)
        dashboard_directory = os.path.join(self.study_directory, "dashboard")
        output_file = os.path.join(dashboard_directory, output_file)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Dashboard available in : {os.path.abspath(output_file)}")
    
    def display(self, rulebase_name = None):
        if rulebase_name is None:
            print("Display of the first rulebase:")
            self.rulebases[0].plot_variables()
            self.rulebases[0].display()
        else:
            all_rulebases_names = os.listdir(self.rulebases_directory)
            idx = all_rulebases_names.index(rulebase_name)
            print("Display of rulebase:" + str(rulebase_name))
            self.rulebases[idx].plot_variables()
            self.rulebases[idx].display()




































