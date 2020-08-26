# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:34:47 2020
@author: gaura
latex src eqns to ".png" images
NOTE: Please change the paths as per your system
"""
import os, json
import subprocess
from shutil import copyfile
from pdf2image import convert_from_path

# creating a template for tex file
def template(eqn, DMOineqn):
    # arranging \DeclareMathOpertaor
    DMOeqn= ''
    for d in DMOineqn:
        DMOeqn += "{} \n".format(d)
    
    '''
    temp ='\\documentclass{standalone}\n' \
               '\\usepackage{amsmath}\n' \
               '\\usepackage{amssymb}\n' \
               f'{k} \n' \
               '\\begin{document}\n' \
               f'$\\displaystyle {{{{ {eqn} }}}} $\n' \
               '\\end{document}'
    '''
    # writing tex document for respective eqn 
    temp1 = '\\documentclass{standalone}\n' \
               '\\usepackage{amsmath}\n' \
               '\\usepackage{amssymb}\n' \
    temp2 = '\\begin{document}\n' \
            f'$\\displaystyle {{{{ {eqn} }}}} $\n' \
            '\\end{document}'
    
    temp = temp1 + DMOeqn + temp2
    return(temp)
		
# paths
base_dir = "/home/gauravs/Automates/results_file"
# Latex_equations directory
latex_equations = os.path.join(base_dir, "latex_equations")
# tex_files dumping directory
tex_files = os.path.join(base_dir, "tex_files")
# directory to dump pdf of the tex files
latex_pdf = os.path.join(base_dir, "latex_pdf")
# directory to dump images of the tex file equations
latex_images = os.path.join(base_dir, "latex_images")
# directory to dump correct latex equations
latex_correct_equations = os.path.join(base_dir, "latex_correct_equations")

# loop through the folders
for folder in os.listdir(latex_equations):
        
    # creating tex, pdf, image folders for each paper
    tex_folder = os.path.join(tex_files, folder)
    pdf_folder = os.path.join(latex_pdf, folder)
    image_folder = os.path.join(latex_images, folder)
    correct_tex_folder = os.path.join(latex_correct_equations, folder)
    for f in [tex_folder, pdf_folder, image_folder, correct_tex_folder]:
        if not os.path.exists(f):
            subprocess.call(['mkdir', f])
                
    # reading eqns of paper from folder in latex_equations 
    path_to_folder = os.path.join(latex_equations, folder)
    main_file = os.path.join(path_to_folder, "latex_equations.txt")
    with open (main_file, 'r') as file:
        eqns = file.readlines()
    # Dealing with "/DeclareMathOperator"
    DMO_file = os.path.join(path_to_folder, "DeclareMathOperator_paper.txt")
    with open(DMO_file, 'r') as file:
        DMO = file.readline()
    
    # initializing /DeclareMathOperator dictionary
    keyword_dict={}
    for i in DMO:
        ibegin, iend = i.find('{'), i.find('}')
        keyword_dict[i[ibegin+1 : iend]] = i
