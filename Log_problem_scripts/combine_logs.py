import os
import subprocess
import fileinput
import json

# re-arranging the logs
def rearranging_logs():

    root = '/projects/temporary/automates/er/gaurav'
    year_list = [14]

    for yr in year_list:
        print(yr)
        year = '20'+str(yr)
        logs_path = os.path.join(root, f'{year}/Logs')

        # Selecting Mathjax_mml logs
        temp = []
        for logFiles in os.listdir(logs_path):
            if 'MathJax_MML_newLock' in logFiles:
                temp.append(logFiles)

        # open and read the files -- merge them together
        os.chdir(logs_path)
        log_data = list(fileinput.input(temp))

        # writing WARNINGs from log_data
        new_log_path = os.path.join(logs_path, f'combine_logs/{year}_MathJax_MML_Log.log')
        FILE = open(new_log_path, 'w')

        for line in log_data:
            if line.split(':')[0] == 'WARNING':
                FILE.write(line)

# calling rearranging_logs function
rearranging_logs()

