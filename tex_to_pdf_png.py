import os, subprocess
from pdf2image import convert_from_path
from shutil import copyfile


# for creating pdf files

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

        command = ['pdflatex','-interaction', 'nonstopmode',os.path.join(tex_folder,texfile)]
        os.chdir(eqn_tex_dst_root)
        output = subprocess.run(command)
        #print(output.returncode)
        #if not output == 0:
         #   os.unlink(f'{i}.pdf')
        os.remove(os.path.join(eqn_tex_dst_root, f'{i}.log'))

        # copying the tex file to the correct latex eqn directory
        if output.returncode==0:
            copyfile(os.path.join(tex_folder,texfile), os.path.join(os.path.join(latex_correct_equations_folder, f"{texfile}")))

        try:
            os.remove(os.path.join(eqn_tex_dst_root, f'{i}.aux'))
        except:
            pass
        #os.remove(os.path.join(eqn_tex_dst_root, f'{i}.log'))

        # copying the tex file to the correct latex eqn directory
        #copy_path = "/home/gauravs/Automates/results_file/latex_correct_equations/{}/{}.tex".format(folder, tex_file)
        #subprocess.call(['cp', os.path.join(tex_folder,texfile), copy_path])

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

