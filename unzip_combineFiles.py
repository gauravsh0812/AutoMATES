# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:48:11 2020

@author: gaura

Unzipping tex files and combining preamble and main tex file 
"""
import os
import json
from subprocess import call, run

# path to the directory having zip files
dir_zip = r"C:\Users\gaura\OneDrive\Desktop\AutoMATES\latex_source\paper1"
os.chdir(dir_zip)

# unzipping the tar files
for index, zipfile in enumerate(os.listdir()):
    
#    # create directory as paper#
#    paper_number = os.join.path(dir_zip, 'paper{}'.format(index))
#    call(['mkdir', paper_number])
#    os.chdir(paper_number)
#    
#    # changing the format
#    zipfile_new = '{}.tar.gz'.format(zipfile)
#    run(['mv', zipfile, zipfile_new])
#    
#    # unzipping the tar file
#    run(['tar -xvzf {}'].format(zipfile_new))
    
# combining the preamble, bibtex, and main tex file --> reanme them main.tex
    # total number of tex files
    tex_files = [file for file in os.listdir() if '.tex' in file]
    
    if len(tex_files) > 1:
        
        files = {}
        # read all the tex files to know which one has \input or \import statement
        for tf in tex_files:
            
            # rank dictionary to rank the multiple tex files in the order they are imported
            rank_dict = {}
            rank_dict[tf] = 0
            
            # reading the tex file
            with open(tf) as TF:
                lines = TF.readlines()
            
            temp = []
            for line_index, line in enumerate(lines):
                if '\\input' in line:
                    # get the imported file name
                    imported_file = line[line.find('{')+1 : line.find('}')]
                    temp.append(imported_file)
            files[tf] = temp
            
        
        # rank the files or arrange them in order
        key_list = list(files.keys()) 
        val_list = list(files.values()) 
        rem_keys = key_list
        
        i = len(key_list)
        for keys in key_list:
            if i >1:
                # check the keys that has no values --> no file imported in this file
                if files[keys] ==[]:
                    val_index = [val_list.index(vl) for vl in val_list if keys in vl][0]
                    CallingFile = key_list[val_index]
                    
                    # open CallingFile and replace the "\input{keys}" --> entire file (as list)
                    os.chdir()
                    with open(CallingFile) as CF:
                        CFlines = CF.readlines
                    with open(keys) as K:
                        Klines = K.readlines
                    
                    for CFl in CFlines:
                        if "\input" in CFl:
                            if CFl[CFl.find('{')+1 : CFl.find('}')] == keys:
                                CFlines.replace(CFl, Klines)
                    
                    # re-writing the opened CallingFile
                    os.chdir()
                    with open(CallingFile, 'w') as CF:
                        json.dump(CFlines, CF, indent=4)
                    
                    # remove the imported file from the files dictionary
                    # also remove it from the values of the file it is imported to
                    del files[keys]
                    
                    old_value = files[CallingFile]
                    new_value = [i for i in old_value if i != keys]
                    files[CallingFile] = new_value
                    i-=1
        
    else:
        # rename the only tex file as main.tex
        src, dst = tex_files[0], 'main_new.tex'
        os.rename(src, dst)
    
        
           #########################################
           
           

    
        
        
    
    
