# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:48:11 2020

@author: gaura

Unzipping tex files and combining preamble and main tex file 
"""
import os
from subprocess import call, run

# path to the directory having zip files
dir_zip = r"C:\Users\gaura\OneDrive\Desktop\AutoMATES\latex_source\paper1"
os.chdir(dir_zip)

# unzipping the tar files
for index, zipfile in enumerate(os.listdir()):
    
    # create directory as paper#
    paper_number = os.join.path(dir_zip, 'paper{}'.format(index))
    call(['mkdir', paper_number])
    os.chdir(paper_number)
    
    # changing the format
    zipfile_new = '{}.tar.gz'.format(zipfile)
    run(['mv', zipfile, zipfile_new])
    
    # unzipping the tar file
    run(['tar -xvzf {}'].format(zipfile_new))
    
# combining the preamble, bibtex, and main tex file --> reanme them main.tex
    # total number of tex files
    tex_files = [file for file in os.listdir() if '.tex' in file]
    
    if len(tex_files) > 1:
        
        files = {}
        # read all the tex files to know which one has \input or \import statement
        for tf in tex_files:
            with open(tf) as TF:
                lines = TF.readlines()
            
            temp = []
            for line_index, line in enumerate(lines):
                if '\\input' in line:
                    # get the imported file name
                    imported_file = line[line.find('{')+1 : line.find('}')]
                    temp.append([line_index, imported_file])
            
            files[tf] = temp
                
        # files.keys() --> main.tex
        # replace all the \input statements with the respective files in main tex file
        main_file = [i for i in files.keys() if len(files[i]) !=0]
        for mf in main_file:
            with open(mf) as main:
                main_lines = main.readlines()
            
            for n in range(len(files[f])):
                main_line_index = files[f][n][0]
                file_to_replace = files[f][n][1]
                
                # checking index of file_to_replace in the tex_files
                t_index = tex_files.index('{}.tex'.format(file_to_replace))
                with open(tex_files[t_index]) as ftr:
                    ftr_lines = ftr.readlines()
                
                f_temp = []
                for ff_index, ff_line in enumerate(ftr_lines):
                    if ff_index != main_line_index:
                        f_temp.append(ff_line)
                    else:
                        for iff in ftr_lines:
                            f_temp.append(iff)
                    
                f = f_temp
        
        os.chdir(paper_number)
        src, dst = main_file, "main.tex"
        os.rename(src, dst)
        
        
    else:
        # rename the only tex file as main.tex
        src, dst = tex_files[0], 'main.tex'
        os.rename(src, dst)
    
        
            
