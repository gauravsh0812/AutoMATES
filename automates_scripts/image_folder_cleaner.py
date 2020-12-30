import os

def Cleaner(path):

    for FOLDER in os.listdir(path):
        
        Folder_path = os.path.join(path, FOLDER)
        
        for Type_of_Folder in ['Large_eqns', 'Small_eqns']:
            
            __path = os.path.join(Folder_path, Type_of_Folder)
            
            os.chdir(__path)
           # print(__path)

            for FILE in os.listdir(__path):
                
                filename = FILE.split(".")[0]
                file_extension = FILE.split(".")[1]
                
                
                if file_extension == 'pdf' or file_extension == 'log' or file_extension == 'aux':
                    os.remove(FILE)
                if file_extension == 'png':
                    if '-' in filename:
                        os.remove(FILE)


if __name__ == '__main__':
    
    for DIR in [1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612]:
        DIR = str(DIR)
        print(DIR)
        path = f'/projects/temporary/automates/er/gaurav/2016/{DIR}/latex_images'
        Cleaner(path)
