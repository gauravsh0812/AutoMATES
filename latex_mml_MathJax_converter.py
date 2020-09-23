import requests
import subprocess, os
import json
import argparse


def main(eqn_file, mml_path):
    # Define the webservice address
    webservice = "http://localhost:8081"
    #print("eqn --> %s" %eqn)
    # Load the LaTeX string data
    #with open(eqn, "rb") as e:
    latex_strs = json.load(open(eqn_file, "r"))
    #print("latex_strs --> %s"%latex_strs)

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

    root = "/home/gauravs/Automates/results_file"
    Latex_strs_json = []
    # path to directory containing correct latex eqns
    folder_correct_latex_eqns = os.path.join(root, "latex_correct_equations")
    # path to directory contain mml eqns
    mml_dir = os.path.join(root, "Mathjax_mml")

    for folder in os.listdir(folder_correct_latex_eqns):
        mml_folder = os.path.join(mml_dir, folder)
        # making folder for each each paper
        if not os.path.exists(mml_folder):
            subprocess.call(['mkdir', mml_folder])

        for eqn in os.listdir(os.path.join(folder_correct_latex_eqns, folder)):
            file_name = eqn.split(".")[0]
            file_path = os.path.join(root, "latex_equations/{}/{}.txt".format(folder, file_name))
            print(file_path)
            text_eqn = open(file_path, "r")
            Latex_strs_json.append(text_eqn.readlines()[0])

        # read the text version of this eqn in latex_eqns file
        #text_eqn = open("file_path", "r")
        print("Latex strs json arry --> {}".format(Latex_strs_json))
        json.dump(Latex_strs_json, open(os.path.join(root, "jsonFile.txt"),"w"))

        # calling main(arg1, arg2) --> arg1: path to json file containing latex eqns
        # args2: path to the json file to store converted mml eqns.
        main(os.path.join(root,"jsonFile.txt"), os.path.join(mml_folder, "MathJax_mml_codes.txt"))
