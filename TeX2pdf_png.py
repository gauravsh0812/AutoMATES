# pdf and png
import os, subprocess
from pdf2image import convert_from_path
from shutil import copyfile
from func_timeout import func_timeout, FunctionTimedOut

# for creating pdf files 
def run_pdflatex(tex_folder, texfile):
    command = ['pdflatex','-interaction', 'nonstopmode',os.path.join(tex_folder,texfile)]
    output = subprocess.run(command)
    return output
    
path = "/home/gauravs/Automates/results_file"
TexFolderPath = os.path.join(path, "tex_files")
for folder in os.listdir(TexFolderPath):
    
    # make latex_correct_eqn folder
    latex_correct_equations_folder = os.path.join(path, f"latex_correct_equations/{folder}")
    if not os.path.exists(latex_correct_equations_folder):
        subprocess.call(['mkdir',latex_correct_equations_folder])

    # make results PDF directory
    eqn_tex_dst_root = os.path.join(path, f"latex_pdf/{folder}")
    if not os.path.exists(eqn_tex_dst_root):
        subprocess.call(['mkdir', eqn_tex_dst_root])

    tex_folder = os.path.join(path, f"tex_files/{folder}")
    for texfile in os.listdir(tex_folder): 
        i = texfile.split(".")[0]
        #print("texfile --> {}".format(texfile))

        #command = ['pdflatex','-interaction', 'nonstopmode',os.path.join(tex_folder,texfile)]
        OutFlag = False
        try:
            os.chdir(eqn_tex_dst_root)
            output = func_timeout(5, run_pdflatex, args=(tex_folder, texfile))#subprocess.run(command)
            OutFlag = True
            
            # Removing log file
            os.remove(os.path.join(eqn_tex_dst_root, f'{i}.log'))
            
        except FunctionTimedOut:
            print("%s couldn't run within 5 sec"%texfile)

        # copying the tex file to the correct latex eqn directory
        if OutFlag:
            if output.returncode==0:
                copyfile(os.path.join(tex_folder,texfile), os.path.join(os.path.join(latex_correct_equations_folder, f"{texfile}")))
            else:
                # Getting line number of the incorrect equation from Eqn_LineNum_dict dictionary got from ParsingLatex
                # Due to dumping the dictionary in ParsingLatex.py code, we will treating the dictionary as text file.
                Paper_Eqn_number = "{}_{}".format(folder, texfile.split(".")[0])  # Folder#_Eqn# --> e.g. 1401.0700_eqn98
                Eqn_Num = "{}".format(texfile.split(".")[0])   # e.g. eqn98
                Index = [i for i,c in enumerate(Eqn_LineNum[0].split(",")) if Eqn_Num in c] # Getting Index of item whose keys() has eqn#
                Line_Num = Eqn_LineNum[0].split(",")[Index[0]].split(":")[1].strip() # Value() of above Keys()
                IncorrectPDF[Paper_Eqn_number] = Line_Num
        else:
            # If file couldn't execute within 5 seconds
            Paper_Eqn_number = "{}_{}".format(folder, texfile.split(".")[0])
            Eqn_Num = "{}".format(texfile.split(".")[0])
            Index = [i for i,c in enumerate(Eqn_LineNum[0].split(",")) if Eqn_Num in c]
            Line_Num = Eqn_LineNum[0].split(",")[Index[0]].split(":")[1].strip()
            IncorrectPDF[Paper_Eqn_number] = Line_Num

        try:
            # Removing aux file if exist
            os.remove(os.path.join(eqn_tex_dst_root, f'{i}.aux'))
        except:
            pass

# Dumping IncorrectPDF logs
json.dump(IncorrectPDF, open("/home/gauravs/Automates/results_file/IncorrectPDFs.txt","w"), indent = 4)

'''
# creating image files
image_directory = "/home/gauravs/Automates/results_file/latex_images"
pdf_directory = "/home/gauravs/Automates/results_file/latex_pdf"
for pdf_folder in os.listdir(pdf_directory):
    path_to_folder = os.path.join(pdf_directory, pdf_folder)
    # mkdir for images of the pdf_folder
    path_to_image_folder = os.path.join(image_directory, pdf_folder)
    print(pdf_folder)
    try:
        if not os.path.exists(path_to_image_folder):
            subprocess.call(["mkdir", path_to_image_folder])

        for index, pdf in enumerate(os.listdir(path_to_folder)):
            print(['pdf_folder --> {}; pdf_file --> {}'.format(pdf_folder, pdf)])
            # extracting the image of the pdf
            if pdf.split(".")[1] == "pdf":
                path_to_pdf = os.path.join(path_to_folder, pdf)
                output_file = '{}.png'.format(pdf.split(".")[0])
                image_folder = path_to_image_folder
                #os.chdir(image_folder)
                img = convert_from_path(path_to_pdf, fmt = 'png', output_folder = image_folder, output_file=output_file)
    except:
        print("wrong pdf file")
'''
