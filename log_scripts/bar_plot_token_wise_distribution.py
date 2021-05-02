import os, json 
import matplotlib.pyplot as plt

# counters
zero_token = 0
one2three_tokens = 0
four2five_tokens = 0
six2ten_tokens = 0
ten_or_more = 0


for m in ['01','02','03','04','05','06','07','08','09','10','11','12']:
    month = '15'+m
    root = f'/projects/temporary/automates/er/gaurav/2015/eqn_token_distribution/{month}/'
    
    for folder in os.listdir(root):
        print(folder)
        for tyf in os.listdir(os.path.join(root, f'{folder}')):
            for json_file in os.listdir(os.path.join(root, f'{folder}/{tyf}')):
                
                #number_of_tokens = json.load(os.path.join(root, f'{folder}/{tyf}/{json_file}'))
                if '.json' in json_file:
                    try:
                        #number_of_tokens = json.load(os.path.join(root, f'{folder}/{tyf}/{json_file}'))
                        number_of_tokens = open(os.path.join(root, f'{folder}/{tyf}/{json_file}'), 'r').readlines()[0]
#                        print(number_of_tokens)
                        if int(number_of_tokens) == 0:
                            zero_token+=1
                        elif 1 <= int(number_of_tokens) <=3:
                            one2three_tokens+=1
                        elif 4<= int(number_of_tokens) <=5:
                            four2five_tokens+=1
                        elif 6<= int(number_of_tokens) <=10:
                            six2ten_tokens+=1
                        else: ten_or_more+=1
                    except:pass

#def bin_plot():

temp = {}
temp['0'] = zero_token
temp['1-3'] = one2three_tokens
temp['4-5'] = four2five_tokens
temp['6-10'] = six2ten_tokens
temp['10+'] = ten_or_more

# plot histogram
plt.figure(figsize=(15,5))
plt.bar(temp.keys(), temp.values(), color='g')
plt.savefig('/projects/temporary/automates/er/gaurav/token_equation_distribution.png')


