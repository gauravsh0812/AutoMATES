# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:34:47 2020

@author: gaura

latex src eqns to ".png" images

NOTE: Please change the paths as per your system
"""
import os, json
from subprocess import call, run
from pdf2image import convert_from_path


# initializing an array to store corect eqns
src_latex_correct_eqns = []

# creating a template for tex file
def template(eqn, k):
    
    temp ='\\documentclass{standalone}\n' \
               '\\usepackage{amsmath}\n' \
               '\\usepackage{amssymb}\n' \
               f'{k} \n' \
               '\\begin{document}\n' \
               f'$\\displaystyle {{{{ {eqn} }}}} $\n' \
               '\\end{document}'
    return(temp)

   

n_papers = 6
for n_paper in range(1,n_papers):
    
    # creating tex, pdf, image dir
    tex_paper = r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\REPO\src_mml_converter\eqn\tex\tex_files\paper{}'.format(n_paper)
    call(['mkdir', tex_paper])
    pdf_paper = r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\REPO\src_mml_converter\eqn\tex\pdf_files\paper{}'.format(n_paper)
    call(['mkdir', pdf_paper])
    image_paper = r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\REPO\src_mml_converter\eqn\tex\images_1\paper{}'.format(n_paper)
    call(['mkdir', image_paper])
    
    # reading eqns of paper# from src_latex_paper#
    with open (r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\REPO\results_file\paper{}\src_latex_paper{}.txt'.format(n_paper, n_paper), 'r') as file:
        eqns = file.readlines()
    
    # Dealing with "/DeclareMathOperator"
    
    with open(r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\REPO\results_file\paper{}\DeclareMathOperator_paper{}.txt'.format(n_paper, n_paper), 'r') as file:
        DMO = file.readline()
    
    # initializing /DeclareMathOperator dictionary
    keyword_dict={}
    for i in DMO:
        ibegin, iend = i.find('{'), i.find('}')
        keyword_dict[i[ibegin+1 : iend]] = i
    
    
    # creating tex files of the eqns
    for index, eqn in enumerate(eqns):
        
        # checking \DeclareMathOperator
        DeclareMathOperator_in_eqn = [kw for kw in keyword_dict.keys() if kw in eqn]
        
        # creating tex file
        path = r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\REPO\src_mml_converter\eqn\tex\tex_files\paper{}\{}.tex'.format(n_paper, index)
        with open(path, 'w') as f_input:
            tex_file = f_input.write(template(eqn, DeclareMathOperator_in_eqn))
    
#    # calling the tex files we have just created
#    os.chdir(tex_paper)
#    for i, f in enumerate(os.listdir()):
#        
#        # grabbing respective tex documents
#        file = os.path.join(tex_paper, f)
        
        # running and storing pdf files generated via "pdflatex".
            os.chdir(pdf_paper)
            value = run(['pdflatex', tex_file])
        
        # removing log and aux file
            call(['del', '{}.aux'.format(index)])
            call(['del', '{}.log'.format(index)])            
        
            if value == 0:
                src_latex_correct_eqns.append(eqn) 
            
              # extracting the image of the pdf
                img_path = os.path.join(pdf_paper, '{}.pdf'.format(index)) 
                output_file = '{}.png'.format(index)
                os.chdir(image_paper)
                img = convert_from_path(img_path, fmt = 'png', output_folder = image_paper, output_file=output_file)

# dumping src_latex_correct_eqns as json file
with open(r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\REPO\results_file\src_latex_correct_eqns.txt', 'w') as file:
    json.dump(src_latex_correct_eqns, file, indent = 4)
