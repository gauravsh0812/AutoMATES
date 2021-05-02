# Parsing all the working tokens
import json
import os
import string

from datetime import datetime


# Printing starting time
print(' ')
start_time = datetime.now()
print('Starting at:  ', start_time)

root = '/projects/temporary/automates/er/gaurav'

def main():
     
    token_set = []
     
    for yr in [14]:#, 15, 16, 17, 18]:
        year = '20' + str(yr)

        for m in ['01']:#,'02','03','04','05','06','07','08','09','10','11','12']:
            month = str(yr)+m
            print(month)
    
            MML_path = os.path.join(root, f'{year}/{month}/Mathjax_mml')

            for folder in os.listdir(MML_path):    
                try:
                    Macros_path = os.path.join(root, f'{year}/{month}/latex_equations/{folder}/Macros_paper.txt')
                    DMO_path = os.path.join(root, f'{year}/{month}/latex_equations/{folder}/DeclareMathOperator_paper.txt')
                    Macros = open(Macros_path, 'r').readlines()
                    DMOs = open(DMO_path, 'r').readlines()
                
                    for tyf in ['Small_MML', 'Large_MML']:
                        tyf_path = os.path.join(MML_path, f'{folder}/{tyf}')
                
                    for eqn in os.listdir(tyf_path):
                        token_set = parsing_token(year, month, folder, Macros, DMOs, tyf, eqn, token_set)
                except:pass
    
    return token_set

def parsing_token(year, month, folder, Macros, DMOs, tyf, eqn, token_set):
        
    try:
        tyf_eqns = 'Small_eqns' if tyf == 'Small_MML' else 'Large_eqns'
        eqn_path = os.path.join(root, f'{year}/{month}/latex_equations/{folder}/{tyf_eqns}/{eqn}')
        equation = open(eqn_path, 'r').readlines()[0]
        
        alphabet_Set = list(string.ascii_lowercase)+list(string.ascii_uppercase)
        
        
        temp_token_list = get_token(alphabet_Set, equation)    
        
        for token in temp_token_list:
    
            temp_token='{'+token+'}'
                
            for macro in Macros:
            
                if temp_token in macro:
                    #print(' -->  ', macro)
                    temp_macro = macro[macro.find(temp_token)+len(temp_token):]
                    try:
                        token = get_token(alphabet_Set, temp_macro)[0] 
                        if token not in token_set:        
                              token_set.append(token)
                    except:pass
                    
                else:
                    if token not in token_set:        
                        token_set.append(token)
                        
    except:pass
    return token_set
            
def get_token(alphabet_Set, equation):   
    
    char_list=[char for char in equation]
    temp_token_list = []
    i, begin, end, alpha = 0,0,0, False
    
    while i <len(char_list):
        
        if char_list[i] in "\\":
            begin =i
            alpha=True
        
        if alpha==True:
            if i!=len(char_list)-1:
                if char_list[i+1] not in alphabet_Set:
                    alpha=False
                    end=i
                    token = equation[begin:end+1]
                    #print(token)
                    temp_token_list.append(token)
        i+=1
    
    return temp_token_list
    
if __name__ == '__main__':
    
    token_set = main()
    
    print(token_set)
    json.dump(token_set, open('/projects/temporary/automates/er/gaurav/working_token_set.json', 'w'))
    
    # Printing stoping time
    print(' ')
    stop_time = datetime.now()
    print('Stoping at:  ', stop_time)
    