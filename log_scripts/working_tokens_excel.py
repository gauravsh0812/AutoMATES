import os, json
import pandas as pd

root = '/projects/temporary/automates/er/gaurav'
path = '/home/gauravs/Automates/temp/Learn_git/Latex_symbols.xlsx'

excel_file = pd.read_excel(path, 'MathJax_Packages')

packages = excel_file.iloc[:,0]#.values()

#token_set = open(os.path.join(root, 'working_tokens_set.json'), 'r').readlines()
token_excel=[]

for p in packages:
    pack = p
    if pack not in token_excel:
        token_excel.append(pack)

#unique_supported_packages = token_excel #+token_set

# check if token_set has any repeated tokens
'''
seen = set()
unique_token = []

for u in unique_supported_packages:
    if u not in seen:
        unique_token.append(u)
        seen.append(u)
'''
json.dump(token_excel, open(os.path.join(root, 'unique_working_tokens.json'), 'w'))

print('Done!!')
print(' ') 
