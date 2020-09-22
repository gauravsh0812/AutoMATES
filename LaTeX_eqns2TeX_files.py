# CREATING TEX FILES OF THE LATEX EQUATIONS 

import os, subprocess

def template(eqn, DMOineqn, Macroineqn):
    # arranging \DeclareMathOpertaor
    
    DMOeqn= ''
    for d in DMOineqn:
        DMOeqn += "{} \n".format(d)
    
    Macroeqn= ''
    for m in Macroineqn:
        Macroeqn += "{} \n".format(m)
    
    # writing tex document for respective eqn 
    temp1 = '\\documentclass{standalone}\n' \
               '\\usepackage{amsmath}\n' \
               '\\usepackage{amssymb}\n' 
    temp2 = '\\begin{document}\n' \
            f'$\\displaystyle {{{{ {eqn} }}}} $\n' \
            '\\end{document}'
    
    temp = temp1 + Macroeqn + DMOeqn + temp2
    return(temp)

# function to create tex documents for each eqn in the folder
def CreateTexDoc(eqns, keyword_dict, keyword_Macro_dict, tex_folder):
    # creating tex files of the eqns
    for index, eqn in enumerate(eqns):
        # checking \DeclareMathOperator and Macros
        DeclareMathOperator_in_eqn = [kw for kw in keyword_dict.keys() if kw in eqn]
        Macros_in_eqn = [kw for kw in keyword_Macro_dict.keys() if kw in eqn]
        # creating tex file
        path_to_tex = os.path.join(tex_folder, "eqn{}.tex".format(index))
        with open(path_to_tex, 'w') as f_input:
            tex_file = f_input.write(template(eqn, DeclareMathOperator_in_eqn, Macros_in_eqn))
            f_input.close()
