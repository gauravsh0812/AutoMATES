# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 23:02:49 2020

@author: gauravs

Latex eqns Parsing code

NOTE: Please change the paths as per your system before running the code.
"""

import pandas as pd
import json, os
from subprocess import call

##########################################################################################################################################
# Parsing latex equations
##########################################################################################################################################


''' these are the three main output array we want, 
-> array of src_mml dictionaries, 
-> array of src latex equations, and 
-> array of the mathml code --> mml
'''
matrix_cmds   = ['{matrix}', '{matrix*}', '{bmatrix}', '{bmatrix*}', '{Bmatrix}', '{Bmatrix*}', '{vmatrix}', '{vmatrix*}', '{Vmatrix}', '{Vmatrix*}']
equation_cmds = ['{equation}', '{equation*}', '{align}', '{align*}', '{eqnarray}', '{eqnarray*}', '{displaymath}']

# get symbols and greek letter 
excel_file = '/home/gauravs/Automates/automates_scripts_new/automates_scripts/Latex_symbols.xlsx'
df = pd.read_excel(excel_file, 'rel_optr')
relational_operators = df.iloc[:, 1].values.tolist()
df_greek = pd.read_excel(excel_file, 'greek')
greek_letters = df_greek.iloc[:, 0].values.tolist()

# looping through the latex paper directories
dir_path = '/home/gauravs/Automates/LaTeX_src/single_tex_1401'
os.chdir(dir_path)
for tex_folder in os.listdir(dir_path):
    
    # to find inline equations i.e. $(...)$
    def inline(length, line):
        pos = [pos for pos, char in enumerate(line) if char == "$"]
        #print(pos, length)
        if length%2 == 0:
            i = 0
            if length > 2:
                while i < length:
                    #print(i)
                    inline_equation = line[pos[i]+1 : pos[i+1]]
                    i = i+2
                    return(inline_equation)
    
            else:
                inline_equation = line[pos[i]+1 : pos[i+1]]
                return(inline_equation)
    
    # to find \[---\] equations
    def bracket_equation(line):
        pos_begin = [pos for pos, char in enumerate(line) if char == "\\["]
        pos_end = [pos for pos, char in enumerate(line) if char == "\\]"]
    
        for i, j in zip(pos_begin, pos_end):
            equation = line[i+1 : j]
            
            return(equation)
    
    # to find \(---\) equations
    def parenthesis_equation(line):
        pos_begin = [pos for pos, char in enumerate(line) if char == "\\("]
        pos_end = [pos for pos, char in enumerate(line) if char == "\\)"]
        
        for i, j in zip(pos_begin, pos_end):
            parenthesis= line[i+1 : j]
        
            return(parenthesis)
    
    # replacing macros with their expanded form
    def Macros(macro_eq, macro_dict):
         
        # first spot the greek letters to avoid confusion in between macros and greek letters
        gl_arr = [gl for gl in greek_letters if gl in macro_eq]
        gl_list = []
        for gl in gl_arr:
            gl_list += list(range(macro_eq.find(gl), macro_eq.find(gl)+len(gl)))
        
        macro_in_eqn = {}
        macro_posi = {}
        for macro in macro_dict.keys():
            if macro in macro_eq:
                print([macro, macro_eq.find(macro)])
                macro_posi[macro] =  macro_eq.find(macro)  # position dictionary of macros
                macro_in_eqn[macro] = macro_dict[macro] # expanded form dictionary of macros
                
        #removing any possible macro which is a part of greek_letters
        if len(macro_posi)!=0:
            mp = [mp for mp in macro_posi.values() if mp in gl_list]
            if len(mp)!=0:
                macro_in_eqn.pop((list(macro_posi.keys())[list(macro_posi.values()).index(mp[0])]))
             
            # initializing an indicator flag --> to check if there will be change in the equation
            indicator = False
            
            for m in macro_in_eqn.keys():
            # replacing the macros with parameters
                if m in macro_eq and '#' in macro_in_eqn[m]:
                    try:
                        ff = macro_in_eqn[m]
                        if ff.find('{') != 0:
                            n_var = int(ff[1]) 

                    #check the number of parameter given upfront and grab that parameter 
                        n_var_upfront = (ff.find('{')//3) - 1
                        var_upfront = [ff[1+i*3] for i in range(1, n_var_upfront) if n_var_upfront !=0]

                    #check the number of parameter given in the eqn and grab those parameter 
                        n_var_rem = n_var - n_var_upfront
                        n_loop = 0
                        var_eqn = []
                        eq_copy = macro_eq
                        b = eq_copy.find(m)
                        b_end = b+len(m)
                        eq_copy = eq_copy[b_end: ]
                        while n_loop < n_var_rem:
                            eq_part1 = eq_copy.find("{")
                            eq_part11 = eq_copy.find("}")
                            var_eqn.append(eq_copy[eq_part1 +1 : eq_part11])
                            eq_copy = eq_copy[eq_part11+1 : ]
                            n_loop+=1

                        list_var = var_upfront + var_eqn 

                #make a dictionaries having parameters and there values
                        temp_macro_dict = {}
                        for a_ind, a in enumerate(list_var):
                            temp_macro_dict['#{}'.format(a_ind+1)] = a 
                
                # replace the macro with the expanded form
                        ff = ff[ff.find('{'): ]    
                        for tmd in temp_macro_dict.keys():
                            if tmd in ff:
                                ff = ff.replace(tmd, temp_macro_dict[tmd])

                        macro_eq = macro_eq.replace(m,ff)
                        indicator = True

                    except:
                            print("MACRO are in wrong format")
            
            # replacing the macros with no parameters
                 elif m in macro_eq and '#' not in macro_in_eqn[m]:
                    try:
                        macro_eq = macro_eq.replace(m, macro_in_eqn[m])
                        #print(m)
                        indicator = True
                                            
                    except:
                        print("MACRO is in the wrong format")
            
            # there are no actual macros to replace --> i.e. all were a part of greek letters       
                else:
                    indicator = False
            
            return(macro_eq, indicator)
        
        # if length of macro_posi = 0    
        else:
            indicator = False
            return(macro_eq, indicator)
    
    # cleaning eqn - part 1 --> removing label, text, intertext
    def Clean_eqn_1(eqn_1):
        
        keywords_tobeCleaned = ["\\label", "\\text", "\\intertext"]
        for KC in keywords_tobeCleaned:
            if KC in eqn_1:
                p = 0
                while p == 0:
                    b = eqn_1.find(KC)
                    count = 1
                    k = 5
                    while count != 0:
                        if eqn_1[b+k] == "}":
                            count = 0 
                        else: 
                            k+=1
                    eqn_1 = eqn_1.replace(eqn_1[b:b+k+1], '')
                    if KC not in eqn_1:
                        p = 1
        return eqn_1 
      
    #removing non-essential commands
    def Clean_eqn_2(eqn_2):
        
        if "\n" in eqn_2:
            eqn_2=eqn_2.replace('\n', '')
        if "%" in eqn_2:
            eqn_2=eqn_2.replace('%', '')
        if "\r" in eqn_2:
            eqn_2=eqn_2.replace('\r', '')
        if "\\bm" in eqn_2:
            eqn_2 =  eqn_2.replace("\\bm", '')
        if "&&" in eqn_2:
            eqn_2=eqn_2.replace('&&', '')
        
        # we don't want "&" in the equation as such untill unless it is a matrix
        if "&" in eqn_2:
            indicator = False
            for mc in matrix_cmds:
                bmc = "\\begin{}".format(mc)
                print(bmc)
                emc = "\\end{}".format(mc) 
                print(emc)
                
                if bmc in eqn_2:
                    indicator = True
                    bmc_index = eqn_2.find(bmc)
                    emc_index = eqn_2.find(emc)
                    len_mc = len(mc)
                    
                    print([bmc_index, emc_index, len_mc])
                
                    
                # spot the index of "&"
                    list_of_and_symbol = [index_ for index_ ,char in enumerate(eqn_2) if char == "&"]     
                    print(list_of_and_symbol)
                # index of the code in between bmc_index to emc_index 
                # don't need to remove "&" from this part eqn
                    index_nochange = list(range(bmc_index+ 6+ len_mc+ 1, emc_index))
                    print(index_nochange)
                    
                # anywhere except index_nochange --> replace the "&" with ''   
                    for los in list_of_and_symbol:
                        if eqn_2[los] == "&" and los not in index_nochange:
                            eqn_2[los] = ''
                
            if not indicator:
                eqn_2=eqn_2.replace('&', '')
        
        return eqn_2
    
    # creating a table having the mathml_output, latex code
    latexCode_arr = []
    mathml_output_arr = []
    def DataSet(mathml_output, latex_code):
        mathml_output_arr.append(mathml_output)
        latexCode_arr.append(latex_code)
    
    def List_to_Str(eqn, encoding):
        if type(eqn) is not list:
            print(type(eqn))
            return list
        else:
            # initialize an empty string
            s = ""
            for ele in eqn:
                ele = ele.decode(encoding, errors = "ignore")#("utf-8")
                s += ele
            return s
    
    # finding the correct Tex document
#    DIR = r'C:\Users\gaura\OneDrive\Desktop\AutoMATES\latex_source\paper{}'.format(n_paper)
#    for Dir in os.listdir(DIR):
#        if "." in Dir:
#            if Dir.split(".")[1] == "tex":
#                Tex_doc = os.path.join(DIR, Dir)
#            elif Dir.split(".")[1] == "cls":
#                    LaTeX_doc = Dir
#    
    tex_file = [file for file in os.listdir(tex_folder)]
    Tex_doc = tex_file[0]
    # Finding the type of encoding i.e. utf-8, ISO8859-1, ASCII, etc.
    unknown_encoding_tex = []
    encoding = subprocess.check_output(["file", "-i",Tex_doc ]).decode("utf-8").split()[2].split("=")[1]
    print(encoding)

    if "unknown" not in encoding:
        file = open(Tex_doc, 'rb')
        lines = file.readlines()

        # initializing the arrays and variables
        src_latex=[]
        macro_dict = {}
        declare_math_operator = []
        total_equations = []
        #MathML_equations = []
        alpha = 0
        matrix = 0
        dollar = 1
        brac = 1

        # since lines are in bytes, we need to convert them into str    
        for index, l in enumerate(lines):
            line = l.decode(encoding, errors = 'ignore')#"utf-8", errors = 'ignore')

            # extracting MACROS
            if "\\newcommand" in line or "\\renewcommand" in line:
                var = line[line.find("{")+1 : line.find("}")]
                macro_dict[var] = line[line.find("}")+1 : ]          

            # extract declare math operator
            if "\\DeclareMathOperator" in line:
                declare_math_operator.append(line)

            # condition 1.a: if $(....)$ is present
            # condition 1.b: if $$(....)$$ is present --> replace it with $(---)$
            if "$" in line or "$$" in line and alpha == 0:
                if "$$" in line:
                    line = line.replace("$$", "$")

                #array of the positions of the "$"
                length = len([c for c in line if c=="$"])   

                #length of the above array -- no. of the "$"
                # if even -- entire equation is in one line
                # if odd -- equation is going to next line
                # if instead of $....$, $.... is present, and upto next 5 lines
                # no closing "$" can be found, then that condition will be rejected.

                if length % 2 == 0:                          
                    inline_equation = inline(length, line)

                else:
                    # combine the lines 
                    dol = 1
                    while dol<6: #dollar != 0:
                        line = line + lines[index + dol].decode(encoding, errors = "ignore") #("utf-8", errors = 'ignore')
                        if "$$" in line:
                            line = line.replace("$$", "$") 

                        length = len([c for c in line if c=="$"])
                        if length%2 != 0:
                            dol+=1
                        else: 
                            dollar = 0

                    if dol<6:
                        inline_equation = inline(length, line)
                        print("$ : {}".format(index))
                    else:
                        inline_equation = None

                #check before appending if it is a valid equation
                if inline_equation is not None:
                    r=[sym for sym in relational_operators if (sym in inline_equation)]
                    if bool(r):# == True:
                        total_equations.append(inline_equation)


            # condition 2: if \[....\] is present
            if "\\[" in line and alpha == 0:
                length_begin = len([c for c in line if c=="\\["])
                length_end = len([c for c in line if c=="\\]"])

                if length_begin == length_end:
                        Bequations = bracket_equation(line)
                elif length_begin > length_end:
                    # combine the lines 
                    br = 1
                    while brac != 0:
                        line = line + lines[index + br].decode(encoding, errors = "ignore")#("utf-8", errors = 'ignore')
                        length_begin = len([c for c in line if c=="\\["])
                        length_end = len([c for c in line if c=="\\]"])
                        if length_begin == length_end:
                            Bequations = bracket_equation(line)

                            print(Bequations)
                        else:
                            br+=1
                #check before appending if it is a valid equation
                if Bequations is not None:
                    r=[sym for sym in relational_operators if (sym in Bequations)]
                    if bool(r):# == True:
                        total_equations.append(Bequations) 


            # condition 3: if \(....\) is present
            if "\\(" in line and alpha == 0:
                length_begin = len([c for c in line if c=="\\("])
                length_end = len([c for c in line if c=="\\)"])
                if length_begin == length_end:
                        Pequations = parenthesis_equation(line)
                elif length_begin > length_end:
                    # combine the lines 
                    br = 1
                    while brac != 0:
                        line = line + lines[index + br].decode(encoding, errors = "ignore")#("utf-8", errors = 'ignore')
                        length_begin = len([c for c in line if c=="\\("])
                        length_end = len([c for c in line if c=="\\)"])
                        if length_begin == length_end:
                            Pequations = parenthesis_equation(line)
                            #print("\\[] : {}".format(index))
                            #print(equations)
                        else:
                            br+=1
                #check before appending if it is a valid equation
                if Pequations is not None:
                    r=[sym for sym in relational_operators if (sym in Pequations)]
                    if bool(r):# == True:
                        total_equations.append(Pequations) 

            # condition 4: if \begin{equation(*)} \begin{case or split} --- \end{equation(*)} \begin{case or split}
            # comdition 5: if \begin{equation(*)} --- \end{equation(*)}

            for ec in equation_cmds:
                if "\\begin{}".format(ec) in line: #or "\\begin{equation*}" in line or "\\begin{align}" in line or "\\begin{align*}" in line or "\\begin{eqnarray}" in line or "\\begin{eqnarray*}" in line or "\\begin{displaymath}" in line:
                    begin_index_alpha = index+1
                    alpha = 1 
                    #print("\\begin eqtn : {}".format(index))

            for ec in equation_cmds:
                if "\\end{}".format(ec) in line and alpha == 1 : # or "\\end{equation*}" in line or "\\end{align}" in line or "\\end{align*}" in line or "\\end{eqnarray}" in line or "\\end{eqnarray*}" in line or "\\end{displaymath}" in line :
                    end_index_alpha = index
                    alpha =0
                    #print("\\endeqtn : {}".format(index))

                    equation = lines[begin_index_alpha : end_index_alpha]
                    eqn = ''
                    for i in range(len(equation)):
                        eqn = eqn + equation[i].decode(encoding, errors = "ignore")#('utf-8')
                    total_equations.append(eqn)



            # condition 6: if '\\begin{..matrix(*)}' but independent under condition 4
            for mc in matrix_cmds:
                if "\\begin{}".format(mc) in line and alpha == 0:
                    matrix = 1
                    begin_matrix_index = index
                    print("\\begin mat : {}".format(index))

                if "\\end{}".format(mc) in line and matrix == 1:
                    end_matrix_index = index
                    matrix =0
                    #print("\\end mat : {}".format(index))

                    # append the array with the recet equation along with the \\begin{} and \\end{} statements
                    equation = lines[begin_matrix_index : end_matrix_index+1]
                    total_equations.append(equation)


        print(total_equations)

        eq=[]
        for e in total_equations:
            if type(e) is list:
                eq.append(List_to_Str(e, encoding))
            else:
                eq.append(e)

        print(eq)


        for i in range(len(eq)):
            print(i)

            # removing unnecc stuff - label, text, intertext
            par_clean_eq = Clean_eqn_1(eq[i])

            # Replacing macros with their expanded form
            macro_eq = Macros(par_clean_eq, macro_dict)

            # removing unnecc stuff -- if indicator = True i.e. MACROs are in correct format hence got replaced
            # else: par_clean_eq will be send to Clean_eqn_2
            if indicator:
                cleaned_eq = Clean_eqn_2(macro_eq)
            else:
                cleaned_eq = Clean_eqn_2(par_clean_eq)

            # sending the output to the dictionaries
            if cleaned_eq not in src_latex:
                src_latex.append(cleaned_eq) 

        # creating and dumping the output file for each paper seperately --> src_latex as json file
        paper_dir = '/home/gauravs/Automates/results_file/{}'.format(tex_folder)
        if not os.path.exists(paper_dir):
            call(['mkdir', paper_dir])

        with open('/home/gauravs/Automates/results_file/{}/latex_equations.txt'.format(tex_folder), 'w') as file:
            json.dump(src_latex, file, indent = 4)

        # creating a file and dumping "/DeclareMathOperator" for each paper
        with open('/home/gauravs/Automates/results_file/{}/DeclareMathOperator_paper.txt'.format(tex_folder), 'w') as file:
            json.dump(declare_math_operator, file, indent = 4)
    
    else:
        unknown_encoding_tex.append(tex_folder)
