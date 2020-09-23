import requests
import subprocess, os
import json
import argparse


def main(eqn, mml_path):
    # Define the webservice address
    webservice = "http://localhost:8081"

    # Load the LaTeX string data
    #latex_strs = json.load(open(eqn, "r"))

    # Translate and save each LaTeX string using the NodeJS service for MathJax
    mml_strs = list()
    for latex in eqn:#latex_strs:
        print(latex)
        res = requests.post(
            f"{webservice}/tex2mml",
            headers={"Content-type": "application/json"},
            json={"tex_src": json.dumps(latex)},
        )
        # Save the MML text response to our list
        mml_strs.append(res.text)

    # Dump the MathML strings to JSON
    json.dump(mml_strs, open(mml_path, "w"))


if __name__ == "__main__":
    
    root = "/home/gauravs/Automates/results_file"
    
    # to collectg all teh correct latex eqns as str 
    Latex_strs_json = []
    # path to directory containing correct latex eqns 
    folder_correct_latex_eqns = os.path.join(root, "latex_correct_equations")
    # path to directory contain mml eqns
    mml_dir = os.path.join(root, "Mathjax_mml")
    
    for folder in os.listdir(folder_correct_latex_eqns):
        mml_folder = os.path.join(mml_dir, folder)
        if not os.path.exists(mml_folder):
            subprocess.call(['mkdir', mml_folder])xdeswq21
        for eqn in os.listdir(os.path.join(folder_correct_latex_eqns, folder)):
            file_name = eqn.split(".")[0]
            file_path = os.path.join(root, "latex_equations/{}/{}".format(folder, file_name))
            text_eqn = open("file_path", "r")
            Latex_strs_json.append(text_eqn.readlines())
            # read the text version of this eqn in latex_eqns file 
            #text_eqn = open("file_path", "r")
        json.dump(Latex_strs_json, os.path.join(root, "json_temp.txt"))
        main(os.path.join(root, "json_temp.txt"), os.path.join(mml_folder, f"{file_name}.txt"))
