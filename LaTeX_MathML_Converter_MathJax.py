# CONVERT LaTeX EQUATION TO MathML CODE USING MathJax

import requests
import subprocess, os
import json
import argparse

def main(eqn_file, mml_path):
    # Define the webservice address
    webservice = "http://localhost:8081"
    # Load the LaTeX string data
    latex_strs = json.load(open(eqn_file, "r"))

    # Translate and save each LaTeX string using the NodeJS service for MathJax
    mml_strs = list()
    for latex in latex_strs:
    #latex = latex_strs
        print("latex in eqn --> %s"%latex)

        res = requests.post(
            f"{webservice}/tex2mml",
            headers={"Content-type": "application/json"},
            json={"tex_src": json.dumps(latex)},
             )
        
        # Save the MML text response to our list
        mml_strs.append(res.text)

    # Dump the MathML strings to JSON
    print(f"mml_strings --> {mml_strs}")
    json.dump(mml_strs, open(mml_path, "w"))

if __name__ == "__main__":
    # Paths
    root = "/home/gauravs/Automates/results_file"
    # Path to directory containing correct latex eqns
    folder_correct_latex_eqns = os.path.join(root, "latex_correct_equations")
    # Path to directory contain MathML eqns
    mml_dir = os.path.join(root, "Mathjax_mml")

    for folder in os.listdir(folder_correct_latex_eqns):
        # Array to keep track of the latex eqns 
        Latex_strs_json = []       
        # Creating folder for MathML codes for specific file
        mml_folder = os.path.join(mml_dir, folder)
        if not os.path.exists(mml_folder):
            subprocess.call(['mkdir', mml_folder])
           
        # Appending all the eqns of the folder/paper to Latex_strs_json along with their respective\
        # Macros and Declare Math Operator commands.
        
        # Creating Macros dictionary
        Macro_file = os.path.join(root, f"latex_equations/{folder}/Macros_paper.txt")
        with open(Macro_file, 'r') as file:
            Macro = file.readlines()
            file.close()
        keyword_Macro_dict={}
        for i in Macro:
            ibegin, iend = i.find('{'), i.find('}')
            keyword_Macro_dict[i[ibegin+1 : iend]] = i
        
        # Creating DMO dictionary
        DMO_file = os.path.join(root, f"latex_equations/{folder}/DeclareMathOperator_paper.txt")
        with open(DMO_file, 'r') as file:
            DMO = file.readlines()
            file.close()
        keyword_dict={}
        for i in DMO:
            ibegin, iend = i.find('{'), i.find('}')
            keyword_dict[i[ibegin+1 : iend]] = i
        
        for eqn in os.listdir(os.path.join(folder_correct_latex_eqns, folder)):
            file_name = eqn.split(".")[0]
            file_path = os.path.join(root, "latex_equations/{}/{}.txt".format(folder, file_name))
            text_eqn = open(file_path, "r").readlines()[0]
            Macros_in_eqn = [kw for kw in keyword_Macro_dict.keys() if kw in text_eqn]
            DMOs_in_eqn = [kw for kw in keyword_dict.keys() if kw in text_eqn]
            
            # Writing Macros, DMOs, and text_eqn as one string
            MiE, DiE = "", ""
            for macro in Macros_in_eqn:
                MiE = MiE + macro + " "
            for dmo in DMOs_in_eqn:
                DiE = DiE + dmo + " "    
            final_string = MiE + DiE + text_eqn
            Latex_strs_json.append(final_string)
        
        # Dumping Latex_strs_json
        if not os.path.exists(os.path.join(root, f"JSON_dir/{folder}_MathJax")):
            subprocess.call(["mkdir", os.path.join(root, f"JSON_dir_MathJax/{folder}")])
        json.dump(Latex_strs_json, open(os.path.join(root, f"JSON_dir_MathJax/{folder}/strings.txt"),"w"))

        # calling main(arg1, arg2) --> arg1: path to json file containing latex eqns
        # args2: path to the json file to store converted mml eqns.
        main(os.path.join(root, f"JSON_dir_MathJax/{folder}/strings.txt"), os.path.join(mml_folder, "MathJax_mml_codes.txt"))
