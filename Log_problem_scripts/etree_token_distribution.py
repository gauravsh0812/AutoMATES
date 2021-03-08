import os, glob
import matplotlib.pyplot as plt

from datetime import datetime

print('Starting at:  ', datetime.now())

less_than_five = 0
five_to_ten = 0
eleven_to_twenty = 0
twentyone_to_thirty=0
thirtyone_to_fifty=0
fiftyone_to_eighty=0
eightyone_to_hundred=0
hundredone_to_onefifty=0
onefiftyone_to_twohundred=0
twohundredone_to_threehundred=0
threehundredone_plus=0

for yr in [14, 15, 16, 17, 18]:
    for m in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10','11','12']:
        year = '20'+str(yr)
        month = str(yr)+m
        print(month)
        path =f'/projects/temporary/automates/er/gaurav/{year}/{month}/etree/*'
        #print(glob.glob(path))
        for folder_path in glob.glob(path):
            #print(folder_path)
            for tyf_path in glob.glob(os.path.join(folder_path, '*')):
                #print(tyf_path)
                for file_path in glob.glob(os.path.join(tyf_path, '*')):
                    #print(file_path)
                    data = open(file_path, 'r').readlines()
                    if len(data) < 5:
                        less_than_five+=1
                    elif 5<=len(data)<=10:
                        five_to_ten+=1
                    elif 11<=len(data)<=20:
                        eleven_to_twenty+=1
                    elif 21<=len(data)<=30:
                        twentyone_to_thirty+=1
                    elif 31<=len(data)<=50:
                        thirtyone_to_fifty+=1
                    elif 51<len(data)<=80:
                        fiftyone_to_eighty+=1
                    elif 81<=len(data)<=100:
                        eightyone_to_hundred+=1
                    elif 101<=len(data)<=150:
                        hundredone_to_onefifty+=1
                    elif 151<=len(data)<=200:
                        onefiftyone_to_twohundred+=1
                    elif 201<=len(data)<=300:
                        twohundredone_to_threehundred+=1
                    else:
                        threehundredone_plus+=1

temp = {}
temp['0-5'] = less_than_five
temp['6-10'] = five_to_ten
temp['11-20'] = eleven_to_twenty
temp['21-30'] =twentyone_to_thirty
temp['31-50'] = thirtyone_to_fifty
temp['51-80'] = fiftyone_to_eighty
temp['81-100'] = eightyone_to_hundred
temp['101-150'] = hundredone_to_onefifty
temp['151-200'] = onefiftyone_to_twohundred
temp['201-300'] = twohundredone_to_threehundred
temp['300+'] = threehundredone_plus

print(temp)

# plot histogram
plt.figure(figsize=(25,10))
plt.bar(temp.keys(), temp.values(), color='g')
plt.savefig('/projects/temporary/automates/er/gaurav/etree_token_distribution.png')

print('Stopping at:  ', datetime.now())
