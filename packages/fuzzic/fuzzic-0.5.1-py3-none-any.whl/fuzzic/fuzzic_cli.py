import argparse
import os
import sys
import shutil
import datetime
from fuzzic.study import study

def study_folder(folder_path):

    current_path = os.getcwd()
    study_name = folder_path
    study_folder = os.path.join(current_path, study_name)
    
    study.create_project(study_name = study_name, path = study_folder)
    
    dossier_B = os.path.join(current_path, study_name, "rulebases")
    dossier_A = study_folder
    
    # Nom du script en cours d'exécution, pour l'ignorer
    nom_du_script = study_name
    

    # 3. Parcourir et copier les fichiers
    fichiers_copies = 0
    
    # Liste tous les éléments (fichiers et dossiers) dans le dossier A
    for nom_element in os.listdir(dossier_A):
        chemin_element_A = os.path.join(dossier_A, nom_element)
        
        # Ignorer le script en cours et les dossiers
        if nom_element == nom_du_script:
            #print(f"-> Ignoré (script): {nom_element}")
            continue
        
        if os.path.isfile(chemin_element_A) and (nom_element.lower().endswith('.xml') or nom_element.lower().endswith('.fis')):
            try:
                chemin_destination_B = os.path.join(dossier_B, nom_element)
                shutil.copy2(chemin_element_A, chemin_destination_B)
                os.remove(chemin_element_A)
                #print(f"-> Copié: {nom_element}")
                fichiers_copies += 1
            except Exception as e:
                print(f"Erreur lors de la copie de {nom_element}: {e}")
    
    if fichiers_copies == 0:
        print("No rulebase found in the format XML.")
    else:
        S = study.Study(ref_study = study_name, path = folder_path)
        S.evaluate()
        S.generate_dashboard()


def study_file(file):
    current_path = os.getcwd()
    study_name = os.path.splitext(file)[0]
    destination_path = os.path.join(current_path, study_name)
    file_path = os.path.join(current_path, file)
    if os.path.isdir(destination_path):
        time = datetime.datetime.today().strftime('%d-%m-%Y--%H:%M:%S')
        destination_path = os.path.join(current_path, time + "_" + study_name)
    os.mkdir(destination_path)
    file_path_destination = os.path.join(destination_path, file)
    shutil.copy2(file_path, file_path_destination)
    study_folder(destination_path)


def main():
    parser = argparse.ArgumentParser(
        description="Fuzzic: A library for analyzing and visualizing fuzzy rule bases."
    )
    
    # 1. Add the main positional argument for the path
    parser.add_argument(
        'path',
        type=str,
        help='The path to the file or folder to be analyzed.'
    )

    args = parser.parse_args()
    input_path = args.path

    # 2. Check if the path exists
    if not os.path.exists(input_path):
        sys.exit(f"Error: Path not found: {input_path}")
    
    # 3. Determine if the path is a file or a folder
    if os.path.isdir(input_path):
        study_folder(input_path)
    elif os.path.isfile(input_path):
        study_file(input_path)
    else:
        # Handle cases like broken symlinks, special devices, etc.
        sys.exit(f"Error: The path '{input_path}' is neither a file nor a folder.")

if __name__ == "__main__":
    main()