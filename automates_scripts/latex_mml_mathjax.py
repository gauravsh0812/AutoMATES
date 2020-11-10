
# CONVERT LaTeX EQUATION TO MathML CODE USING MathJax

import requests
import subprocess, os
import json
import argparse
import multiprocessing
import logging 

from multiprocessing import Pool, Lock, TimeoutError

# Defining global lock
lock = Lock()

# Defining the rot directory to store log files
root = f"/projects/temporary/automates/er/gaurav/{dir}_results"

# Setting up Logger - To get log files
Log_Format = '%(levelname)s:%(message)s'

logger_keywords = logging.getLogger(os.path.join( root, 'MathJax_Unsupported_Keywords'))
logger_errors = logging.getLogger(os.path.join(root, 'MathJax_Errors'))

## Setting the levels of loggers
logger_keywords.setLevel(logging.WARNING)
logger_errors.setLevel(logging.WARNING)

## Adding file handler
fh = logging.FileHandler('MathJax_MML.log')
fh.setLevel(logging.WARNING)

## Setting up the format
formatter = logging.Formatter('%(levelname)s: %(message)s')
fh.setFormatter(formatter)

## Add the handlers to logger
logger_keywords.addHandler(fh)
logger_errors.addHandler(fh)



# Defining global dictionary and array to capture all the keywords not supported by MathJax and other erros respectively
#keywords_log =[]
#Errors = []

def main(file_name, final_eqn, tempPath, mml_path):
    
    global lock
    
    # Define the webservice address
    webservice = "http://localhost:8081"
    # Load the LaTeX string data
    #eqn = json.load(open(tempPath, "r"))
    eqn = final_eqn
    
    lock.acquire()
    print(f"in main: {file_name}")
    print(eqn)
    lock.release()
    # Translate and save each LaTeX string using the NodeJS service for MathJax
    
    res = requests.post(
        f"{webservice}/tex2mml",
        headers={"Content-type": "application/json"},
        json={"tex_src": json.dumps(eqn)},
         )
    
    lock.acquire()
    #print(f'Response of the webservice request: {res.text}')
    lock.release()
    
    # Capturing the keywords not supported by MathJax
    if "FAILED" in res.content.decode("utf-8"):
        # Just to check errors
        TeXParseError = res.content.decode("utf-8").split("::")[1]
        # Logging incorrect/ unsupported keywords along with their equations
        if "Undefined control sequence" in TeXParseError:
            Unsupported_Keyword = TeXParseError.split("\\")[-1]
            #if Unsupported_Keyword not in keywords_log:
                #keywords_log.append(Unsupported_Keyword)
            logger_keywords.warning(f'{Unsupported_Keyword} is either not supported by MathJax or incorrectly written.')
            #print("FAILED")
        # Logging errors other than unsupported keywords
        else:
            #if TeXParseError not in Errors:
                #Errors.append(TeXParseError)
            logger_errors.warning(f'{TeXParseError} is an error produced by MathJax webserver.')
                
    else:
        # Cleaning and Dumping the MathML strings to JSON file
        MML = CleaningMML(res.text)
        print(f"writing {file_name}")
        
        MML_output = open(os.path.join(mml_path, f"{file_name}.txt"), "w")
        
        lock.acquire()
        #json.dump(MML, open(os.path.join(mml_path, f"{file_name}.txt"), "w"))
        MML_output.write(MML)
        lock.release()
        
        
def Creating_Macro_DMO_dictionaries(folder):
    
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
    
    return(keyword_Macro_dict, keyword_dict)
    
    # Calling function to create final strings of eqns having respective Macros and DMOs
    #Creating_final_equations(type_of_folder, dir, folder, keyword_Macro_dict, keyword_dict, Large_MML, Small_MML)
    
    

def Creating_final_equations(args_list):
    
    global lock
   
    # Unpacking the args_list
    (type_of_folder, eqn, dir, folder, keyword_Macro_dict, keyword_dict, Large_MML, Small_MML) = args_list
    
    try:
        file_name = eqn.split(".")[0] if '-' not in eqn else eqn.split('-')[0]
        
        print(f'{folder}:{type_of_folder}:{file_name}')
        EqnsType = "Large_eqns" if type_of_folder == Large_eqns else "Small_eqns"
        file_path = os.path.join(root, f"latex_equations/{folder}/{EqnsType}/{file_name}.txt")
        final_eqn = ""
        #try:
        text_eqn = open(file_path, "r").readlines()[0]
        Macros_in_eqn = [kw for kw in keyword_Macro_dict.keys() if kw in text_eqn]
        DMOs_in_eqn = [kw for kw in keyword_dict.keys() if kw in text_eqn]
            
        # Writing Macros, DMOs, and text_eqn as one string
        MiE, DiE = "", ""
        for macro in Macros_in_eqn:
            MiE = MiE + keyword_Macro_dict[macro] + " "
        for dmo in DMOs_in_eqn:
            DiE = DiE +  keyword_dict[dmo] + " "    
        
        string = MiE + DiE + text_eqn
        
        # Removing unsupported keywords 
        for tr in ["\\ensuremath", "\\xspace", "\\aligned", "\\endaligned", "\\span"]:
            string = string.replace(tr, "")
        
        # Correcting keywords written in an incorrect way
        for sub in string.split(" "):
            if "cong" in sub:
                sub = sub.replace("\\cong", "{\\cong}")
            if "mathbb" in sub:
                if sub[sub.find("\\mathbb")+7] != "{":
                    mathbb_parameter = sub[sub.find("\\newcommand")+12 : sub.find("}")].replace("\\", "")
                    sub = sub[:sub.find("\\mathbb")+7] + "{" + mathbb_parameter + "}" + sub[sub.find("\\mathbb")+7+len(mathbb_parameter):]
            if "mathbf" in sub:
                if sub[sub.find("\\mathbf")+7] != "{":
                    mathbf_parameter = sub[sub.find("\\newcommand")+12 : sub.find("}")].replace("\\", "")
                    sub = sub[:sub.find("\\mathbf")+7] + "{" + mathbf_parameter + "}" + sub[sub.find("\\mathbf")+7+len(mathbf_parameter):]
            
            final_eqn += sub + " "     
        
        # Printing the final equation string
        
        lock.acquire()
        #print("final equation is  ", final_eqn)
        lock.release()
        
        # Storing the final equation in a temporary json file
        tempPath = f"/projects/temporary/automates/er/gaurav/{dir}_results/tempFile.txt"
        
        lock.acquire()
        json.dump(final_eqn, open(tempPath, "w"))
        lock.release()
        
        MML = Large_MML if EqnsType == "Large_eqns" else Small_MML
        #print(" ==================================================")
        print(MML)
        main(file_name, final_eqn, tempPath, MML)

    except:
    
        lock.acquire()
        print( " " )
        print(" ======================START============================")
        print(f' {folder}:{type_of_folder}:{file_name} can not be converted.')
        print(" =======================END=============================")
        print( " " )
        lock.release()
            

def CleaningMML(res):

    # Removing "\ and /" at the begining and at the end
    res = res[res.find("<"):]
    res = res[::-1][res[::-1].find(">"):]
    res = res[::-1]
    # Removing "\\n"
    res = res.replace(">\\n", ">")
    return(res)
    

def Pooling(type_of_folder, dir, folder, keyword_Macro_dict, keyword_dict, Large_MML, Small_MML):
    
    temp = []
    
    for index, eqn in enumerate(os.listdir(type_of_folder)):
        
        if '.png' in eqn:
            temp.append([type_of_folder, eqn, dir, folder, keyword_Macro_dict, keyword_dict, Large_MML, Small_MML])    
    
    with Pool(multiprocessing.cpu_count()//2) as pool:
        result = pool.map(Creating_final_equations, temp)
    
    
if __name__ == "__main__":
    
    #for dir in ['1402', '1403', '1404', '1405']:
    dir = '1402'
    root = f"/projects/temporary/automates/er/gaurav/{dir}_results"
    # Path to image directory
    folder_images = os.path.join(root, "latex_images")
    # Path to directory contain MathML eqns
    mml_dir = os.path.join(root, "Mathjax_mml")
    
    #for folder in os.listdir(folder_images):
    folder = "1402.0091"
    # Creating folder for MathML codes for specific file
    mml_folder = os.path.join(mml_dir, folder)
    # Creating folder for Large and Small eqns
    Large_MML = os.path.join(mml_folder, "Large_MML")
    Small_MML = os.path.join(mml_folder, "Small_MML")
    for F in [mml_folder, Large_MML, Small_MML]:
        if not os.path.exists(F):
            subprocess.call(['mkdir', F])
    
    # Creating Macros dictionary
    #keyword_Macro_dict, keyword_dict = Creating_Macro_DMO_dictionaries(folder)
    
    #Appending all the eqns of the folder/paper to Latex_strs_json 
    #along with their respective Macros and Declare Math Operator commands.
    
    # Creating array of final eqns
    Large_eqns = os.path.join(folder_images, f"{folder}/Large_eqns")
    Small_eqns = os.path.join(folder_images, f"{folder}/Small_eqns")
    
    # Creating Macros dictionary
    keyword_Macro_dict, keyword_dict = Creating_Macro_DMO_dictionaries(folder)
    
    for type_of_folder in [Large_eqns, Small_eqns]:
        
        Pooling(type_of_folder, dir, folder, keyword_Macro_dict, keyword_dict, Large_MML, Small_MML)
        
        # array to store pairs of [type_of_folder, folder, Large_MML, Small_MML] Will be used as arguments in pool.map            
        
            
            
          
    #print(keywords_log)
    #print(" ")
    #print(" ====================== Errors ======================")
    #print(" ")
    #print(Errors)
    #json.dump(keywords_log, open("/projects/temporary/automates/er/gaurav/results_file/MathJax_Logs/Keywords_logs.txt", "w"))  
    #json.dump(Errors, open("/projects/temporary/automates/er/gaurav/results_file/MathJax_Logs/Errors_logs.txt", "w"))  

######################################################################

######################################################################
'''
# CONVERT LaTeX EQUATION TO MathML CODE USING MathJax

import requests
import subprocess, os
import json
import argparse

# Defining global dictionary and array to capture all the keywords not supported by MathJax and other erros respectively
keywords_log =[]
Errors = []
count=0

# Removing "\n", "\", and un-necessary qoutes 
def CleaningMML(res):
    # Removing "\ and /" at the begining and at the end
    res = res[res.find("<"):]
    res = res[::-1][res[::-1].find(">"):]
    res = res[::-1]
    # Removing "\\n"
    res = res.replace(">\\n", ">")
    return(res)
    
def Creating_Macro_DMO_dictionaries(folder):
    #print("in Creating_Macro_DMO_dictionaries")
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
    
    return(keyword_Macro_dict, keyword_dict)

def Creating_final_equations(ce, folder, keyword_Macro_dict, keyword_dict, Large_MML, Small_MML):
    #print("in Creating_final_equations")
    for index, eqn in enumerate(os.listdir(ce)):
        if '.png' in eqn:
            #print(eqn)
            file_name = eqn.split(".")[0]
            EqnsType = "Large_eqns" if ce == Large_correct_eqns else "Small_eqns"
            file_path = os.path.join(root, f"latex_equations/{folder}/{EqnsType}/{file_name}.txt")
            final_eqn = ""
            try:
                text_eqn = open(file_path, "r").readlines()[0]
                Macros_in_eqn = [kw for kw in keyword_Macro_dict.keys() if kw in text_eqn]
                DMOs_in_eqn = [kw for kw in keyword_dict.keys() if kw in text_eqn]
                    
                # Writing Macros, DMOs, and text_eqn as one string
                MiE, DiE = "", ""
                for macro in Macros_in_eqn:
                    MiE = MiE + keyword_Macro_dict[macro] + " "
                for dmo in DMOs_in_eqn:
                    DiE = DiE +  keyword_dict[dmo] + " "    
                string = MiE + DiE + text_eqn
                
                # Removing unsupported keywords 
                for tr in ["\\ensuremath", "\\xspace", "\\aligned", "\\endaligned", "\\span"]:
                    string = string.replace(tr, "")
                
                # Correcting keywords written in an incorrect way
                for sub in string.split(" "):
                    if "cong" in sub:
                        sub = sub.replace("\\cong", "{\\cong}")
                    if "mathbb" in sub:
                        if sub[sub.find("\\mathbb")+7] != "{":
                            mathbb_parameter = sub[sub.find("\\newcommand")+12 : sub.find("}")].replace("\\", "")
                            sub = sub[:sub.find("\\mathbb")+7] + "{" + mathbb_parameter + "}" + sub[sub.find("\\mathbb")+7+len(mathbb_parameter):]
                    if "mathbf" in sub:
                        if sub[sub.find("\\mathbf")+7] != "{":
                            mathbf_parameter = sub[sub.find("\\newcommand")+12 : sub.find("}")].replace("\\", "")
                            sub = sub[:sub.find("\\mathbf")+7] + "{" + mathbf_parameter + "}" + sub[sub.find("\\mathbf")+7+len(mathbf_parameter):]
                    
                    final_eqn += sub + " "     
                #print("final_eqn --> %s"%final_eqn)
                
                tempPath = "/projects/temporary/automates/er/gaurav/results_file/tempFile.txt"
                json.dump(final_eqn, open(tempPath, "w"))
                MML = Large_MML if EqnsType == "Large_eqns" else Small_MML
                count+=1
                main(folder, file_name, tempPath, MML)
                
            except:
                pass
    
def main(folder,file_name, tempPath, mml_path):
    #print("main")
    #print(eqn)
    
    # Define the webservice address
    webservice = "http://localhost:8081"
    # Load the LaTeX string data
    eqn = json.load(open(tempPath, "r"))
    #print(eqn)
    #print("++==++"*15)
    # Translate and save each LaTeX string using the NodeJS service for MathJax
    #mml_strs = list()
    
    try:
        res = requests.post(
            f"{webservice}/tex2mml",
            headers={"Content-type": "application/json"},
            json={"tex_src": json.dumps(eqn)},
            timeout = 2
            )
        
        #print(res.text)
        # Capturing the keywords not supported by MathJax
        if "FAILED" in res.content.decode("utf-8"):
            # Just to check errors
            TeXParseError = res.content.decode("utf-8").split("::")[1]
            # Logging incorrect/ unsupported keywords along with their equations
            if "Undefined control sequence" in TeXParseError:
                Unsupported_Keyword = TeXParseError.split("\\")[-1]
                if Unsupported_Keyword not in keywords_log:
                    keywords_log.append(Unsupported_Keyword)
            # Logging errors other than unsupported keywords
            elif "Math Processing Error: Maximum call stack size exceeded" in res.content.decode('utf-8'):
                print(f'{eqn} is not working. Lets PASS this.')
                pass
                
            else:
                if TeXParseError not in Errors:
                    Errors.append(TeXParseError)
                    
        else:
            # Dump the MathML strings to JSON file
            MML = CleaningMML(res.text)
            json.dump(MML, open(os.path.join(mml_path, f"{file_name}.txt"), "w"))
    
    except:
        print(f"OOPS!! {folder}:{file_name} is not working.")
        
if __name__ == "__main__":
    # Paths
    root = "/projects/temporary/automates/er/gaurav/1402_results"
    # Path to directory containing correct latex eqns
    folder_correct_latex_eqns = os.path.join(root, "latex_images")
    # Path to directory contain MathML eqns
    mml_dir = os.path.join(root, "Mathjax_mml")
    
    for folder in os.listdir(folder_correct_latex_eqns):
        # Creating folder for MathML codes for specific file
        mml_folder = os.path.join(mml_dir, folder)
        # Creating folder for Large and Small eqns
        Large_MML = os.path.join(mml_folder, "Large_MML")
        Small_MML = os.path.join(mml_folder, "Small_MML")
        for F in [mml_folder, Large_MML, Small_MML]:
            if not os.path.exists(F):
                subprocess.call(['mkdir', F])
        
        # Creating Macros dictionary
        keyword_Macro_dict, keyword_dict = Creating_Macro_DMO_dictionaries(folder)
        
        #Appending all the eqns of the folder/paper to Latex_strs_json 
        #along with their respective Macros and Declare Math Operator commands.
        # Creating array of final eqns
        Large_correct_eqns = os.path.join(folder_correct_latex_eqns, f"{folder}/Large_eqns")
        Small_correct_eqns = os.path.join(folder_correct_latex_eqns, f"{folder}/Small_eqns")
        for ce in [Large_correct_eqns, Small_correct_eqns]:
            Creating_final_equations(ce, folder, keyword_Macro_dict, keyword_dict, Large_MML, Small_MML)
            
          
    print(keywords_log)
    print(" ")
    print(" ====================== Errors ======================")
    print(" ")
    print(Errors)
    print(" ")
    print(" ====================== Errors ======================")
    print(" ")
    print(count)
    json.dump(keywords_log, open("/projects/temporary/automates/er/gaurav/results_file/MathJax_Logs/Keywords_logs.txt", "w"))  
    json.dump(Errors, open("/projects/temporary/automates/er/gaurav/results_file/MathJax_Logs/Errors_logs.txt", "w"))  

'''