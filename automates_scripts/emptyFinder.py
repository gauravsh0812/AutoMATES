import os, json, shutil 

def main():

        Files_to_check = []

        for DIR in [1405]:

            path = f'/projects/temporary/automates/er/gaurav/2014/{DIR}/Mathjax_mml'
            for Folder in os.listdir(path):
                folder_path = os.path.join(path, Folder)


                Large_path = os.path.join(folder_path, 'Large_MML')
                Small_path = os.path.join(folder_path, 'Small_MML')
                if os.path.exists(Large_path):
                    Large_files = len(os.listdir(Large_path))
                else:
                    Files_to_check.append(Folder) 
                if os.path.exists(Small_path):
                    Small_files = len(os.listdir(Small_path))
                else:
                    Files_to_check.append(Folder) 

                Total = Large_files+Small_files

                if Total == 0:
                    Files_to_check.append(Folder)    

        print(Files_to_check)

if __name__=="__main__":
    main()
