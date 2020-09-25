# RENDERING .png FROM THE pdf FILES OF THE EQUATIONS

import os, subprocess
from pdf2image import convert_from_path

def main(pdf_file_path, pdf_file, image_folder):
    try:
        # extracting the image of the pdf
        output_file = '{}.png'.format(pdf_file.split(".")[0])
        convert_from_path(pdf_file_path, fmt = 'png', output_folder = image_folder, output_file=output_file)
    except:
        pass

if __name__ == "__main__":
    # Paths
    root = "/home/gauravs/Automates/results_file"
    pdf_path = os.path.join(root, "latex_pdf")
    image_path = os.path.join(root, "latex_images")
    
    for fldr in os.listdir(pdf_path):
        # Path to folder containing all pdf files of specific paper
        pdf_folder = os.path.join(pdf_path, fldr)
        # mkdir image folder if not exists
        image_folder = os.path.join(image_path, fldr)
        if not os.path.exists(image_folder):
            subprocess.call(["mkdir", image_folder])
        
        # Looping through pdf files
        for pdf_file in os.listdir(os.path.join(pdf_path, fldr)):
            if pdf_file.split(".")[1] == "pdf":
                pdf_file_path = os.path.join(pdf_folder, pdf_file) 
                main(pdf_file_path, pdf_file, image_folder)
