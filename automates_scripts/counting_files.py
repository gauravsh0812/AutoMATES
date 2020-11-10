import os

root = "/projects/temporary/automates/er/gaurav"

path_1402_ran = os.path.join(root, '1402_results/Mathjax_mml')

# Initializing parameters 
TotalPaper_1401, SingleTex_1401, Unknown_1401, SingleTex_1401_read, Total_eqns_1401, Total_pdfs_1401, Total_mmls_1401 = 0, 0, 0, 0, 0, 0
TotalPaper_1402, SingleTex_1402, Unknown_1402, Total_eqns_1402, Total_pdfs_1402, Total_mmls_1402 = 0, 0, 0, 0, 0, 0



# 1401 dir

for _ in os.listdir("/projects/temporary/automates/arxiv/src/1401"):
    TotalPaper_1401+=1

Unknown_1401 = len(open("/projects/temporary/automates/er/gaurav/results_file/unknown_encoding_tex.txt", "r").readlines[0])
SingleTex_1401 = TotalPaper_1401 - Unknown_1401

for folder in os.listdir(os.path.join(root, 'results_file/latex_equations')):
    SingleTex_1401_read+=1
    for sub_folder in ['Small_eqns', 'Large_eqns']:
        for _ in os.listdir(os.path.join(os.path.join(root, 'results_file/latex_equations'), f'{folder}/{sub_folder}')):
            Total_eqns_1401+=1

for folder in os.listdir(os.path.join(root, 'results_file/latex_pdfs')):
    for sub_folder in ['Small_eqns', 'Large_eqns']:
        for _ in os.listdir(os.path.join(os.path.join(root, 'results_file/latex_pdfs'), f'{folder}/{sub_folder}')):
            Total_pdfs_1401+=1

for folder in os.listdir(os.path.join(root, 'results_file/Mathjax_mml')):
    for sub_folder in ['Small_MML', 'Large_MML']:
        for _ in os.listdir(os.path.join(os.path.join(root, 'results_file/Mathjax_mml'), f'{folder}/{sub_folder}')):
            Total_mmls_1401+=1



# 1402 dir

for _ in os.listdir("/projects/temporary/automates/arxiv/src/1402"):
    TotalPaper_1402+=1

Unknown_1402 = len(open("/projects/temporary/automates/er/gaurav/1402_results/unknown_encoding_tex.txt", "r").readlines[0])
SingleTex_1402 = TotalPaper_1402 - Unknown_1402

for folder in os.listdir(os.path.join(root, '1402_results/latex_equations')):
    SingleTex_1402_read+=1
    for sub_folder in ['Small_eqns', 'Large_eqns']:
        for _ in os.listdir(os.path.join(os.path.join(root, '1402_results/latex_equations'), f'{folder}/{sub_folder}')):
            Total_eqns_1402+=1

for folder in os.listdir(os.path.join(root, '1402_results/latex_images')):
    for sub_folder in ['Small_eqns', 'Large_eqns']:
        for _ in os.listdir(os.path.join(os.path.join(root, '1402_results/latex_images'), f'{folder}/{sub_folder}')):
            Total_pdfs_1402+=1

for folder in os.listdir(os.path.join(root, '1402_results/Mathjax_mml')):
    for sub_folder in ['Small_MML', 'Large_MML']:
        for _ in os.listdir(os.path.join(os.path.join(root, '1402_results/Mathjax_mml'), f'{folder}/{sub_folder}')):
            Total_mmls_1402+=1



# Printing results

print("1401 dir")
print("+++++++++++++++++++++++++++++")
print(" Total number of arXiv papers: ", TotalPaper_1401)
print(" Total number of arXiv papers with single tex file: ", SingleTex_1401)
print(" Total number of arXiv papers with unknown encoding: ", Unknown_1401)
print(" Total number of eqns: ", Total_eqns_1401)
print(" Total number of pdfs: ", Total_pdfs_1401)
print(" Total number of MMLs: ", Total_mmls_1401)

print("1402 dir")
print("+++++++++++++++++++++++++++++")
print(" Total number of arXiv papers: ", TotalPaper_1402)
print(" Total number of arXiv papers with single tex file: ", SingleTex_1402)
print(" Total number of arXiv papers with unknown encoding: ", Unknown_1402)
print(" Total number of eqns: ", Total_eqns_1401)
print(" Total number of pdfs: ", Total_pdfs_1401)
print(" Total number of MMLs: ", Total_mmls_1401)