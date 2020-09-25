# CREATING TEX FILES OF THE LATEX EQUATIONS 

import os, subprocess

# Template for the TeX files
def template(eqn, Preamble_DMO, Preamble_Macro):
    
    # writing tex document for respective eqn 
    temp1 = '\\documentclass{standalone}\n' \
               '\\usepackage{amsmath}\n' \
               '\\usepackage{amssymb}\n' 
    temp2 = '\\begin{document}\n' \
            f'$\\displaystyle {{{{ {eqn} }}}} $\n' \
            '\\end{document}'
    
    temp = temp1 + Preamble_DMO + Preamble_Macro + temp2
    return(temp)

# function to create tex documents for each eqn in the folder
def CreateTexDoc(eqn, keyword_dict, keyword_Macro_dict, tex_folder, TeX_name):
   
    # checking \DeclareMathOperator and Macros
    DeclareMathOperator_in_eqn = [kw for kw in keyword_dict.keys() if kw in eqn]
    Macros_in_eqn = [kw for kw in keyword_Macro_dict.keys() if kw in eqn]
    Preamble_DMO, Preamble_Macro = '', ''
    for d in DeclareMathOperator_in_eqn:
        Preamble_DMO += "{} \n".format(keyword_dict[d])
    for m in Macros_in_eqn:
        Preamble_Macro += "{} \n".format(keyword_Macro_dict[m])
            
    # creating tex file
    path_to_tex = os.path.join(tex_folder, "{}.tex".format(TeX_name))
    with open(path_to_tex, 'w') as f_input:
        f_input.write(template(eqn, Preamble_DMO, Preamble_Macro))
        f_input.close()

def main(latex_equations, tex_files):
    
    # loop through the folders
    for folder in os.listdir(latex_equations):     
        # creating tex, pdf, image folders for each paper
        tex_folder = os.path.join(tex_files, folder)
        if not os.path.exists(tex_folder):
            subprocess.call(['mkdir', tex_folder])
                    
        # reading eqns of paper from folder in latex_equations 
        path_to_folder = os.path.join(latex_equations, folder)
        
        # Dealing with "/DeclareMathOperator"
        DMO_file = os.path.join(path_to_folder, "DeclareMathOperator_paper.txt")
        with open(DMO_file, 'r') as file:
            DMO = file.readlines()
        
        # initializing /DeclareMathOperator dictionary
        keyword_dict={}
        for i in DMO:
            ibegin, iend = i.find('{'), i.find('}')
            keyword_dict[i[ibegin+1 : iend]] = i
        
        # Dealing with "Macros"
        Macro_file = os.path.join(path_to_folder, "Macros_paper.txt")
        with open(Macro_file, 'r') as file:
            Macro = file.readlines()
        
        # initializing /Macros dictionary
        keyword_Macro_dict={}
        for i in Macro:
            ibegin, iend = i.find('{'), i.find('}')
            keyword_Macro_dict[i[ibegin+1 : iend]] = i
        
        for MF in os.listdir(path_to_folder):
            if MF != "DeclareMathOperator_paper.txt" and MF!= "Macros_paper.txt":
                main_file = os.path.join(path_to_folder, MF)
                with open (main_file, 'r') as file:
                    eqn = file.readlines()
                    file.close()
                
                TeX_name = MF.split(".")[0]
                # calling function to create tex doc for the particular folder --> giving all latex eqns, DMOs, Macros and tex_folder path as arguments
                if len(eqn)!=0:
                    CreateTexDoc(eqn[0], keyword_dict, keyword_Macro_dict, tex_folder, TeX_name)

if __name__ == "__main__":
    # paths
    base_dir = "/home/gauravs/Automates/results_file"
    # Latex_equations directory
    latex_equations = os.path.join(base_dir, "latex_equations")
    # tex_files dumping directory
    tex_files = os.path.join(base_dir, "tex_files")
    
    main(latex_equations, tex_files)
