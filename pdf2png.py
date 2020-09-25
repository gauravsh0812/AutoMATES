
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

