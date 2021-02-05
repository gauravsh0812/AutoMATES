import os, json 

set1_path = '/projects/temporary/automates/er/gaurav/working_token_set.json'
set2_path = '/projects/temporary/automates/er/gaurav/unique_working_tokens.json'

nw_set = set()
#nw_token = []

working_set = set()
#working_token = []

# combine not_working_tokens
for yr in [14, 15, 16, 17, 18]:
    year = '20'+str(yr)
    path = f'/projects/temporary/automates/er/gaurav/{year}/Logs/combine_logs/not_working_tokens.json'
    with  open(path, 'r') as fp:
        data = json.load(fp)

    for key in (data.keys()):
        if key not in nw_set:
            nw_set.add(key)
            #nw_token.append(key)

# combine working_tokens
for s in [set1_path, set2_path]:
    with open(s, 'r') as fp:
        sdata = json.load(fp)

    for t in sdata:
        if t not in working_set:
            working_set.add(t)
            #working_token.append(t)

# get difference of wokring and not_working_tokens
diff = list(nw_set - working_set)

# storing diff list
json.dump(diff, open('/projects/temporary/automates/er/gaurav/difference_tokens_set.json', 'w'))
