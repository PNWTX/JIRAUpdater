#https://developer.atlassian.com/cloud/jira/platform/rest/v2/intro/#expansion
#https://community.atlassian.com/t5/Jira-questions/Python-API-update/qaq-p/1242523

from jira import JIRA, Priority 
import os
import pandas as pd
import pwinput

##### Selects current directory of file as source for reading other files #####
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
os.system('cls')

##### Read .csv file into Pandas data frame for uploading to JIRA #####
try:
    df = pd.read_csv(r'2023-02.csv', header=None) #File name needs to match this line
except:
    print('File not found. Re-run program once file is available in folder with script.')
    print(' ')
    exit()
#print(df) #For dataframe auditing purposes

##### Requests Basic Authorization Credentials for Connecting to JIRA #####
print('Enter Username:',end=' ')
username = input()
print('Enter Password:',end=' ')
password = pwinput.pwinput(prompt='',mask='*')
print(' ')
try:
    jira = JIRA(server="https://jira.yourserver.com", basic_auth=(username, password)) #need to update 'yourserver' to a production server to work!
except:
    print('Authentication Failed. Re-run program with correct credentials.')
    print(' ')
    quit()
os.system('cls')

print('Program running and values updating in JIRA......')
print(' ')
fail = 0 #Starts counter for number of failed JIRAs (i.e. couldn't be accessed / don't exist)
##### Loops through every row of the CSV and updates the fields in JIRA #####
for row in df.index:
    ##### Assigns JIRA key to update for each iteration #####
    issuekey = df.iloc[row,0]
    try:
        issue = jira.issue(issuekey)
        ##### Updates  Period 1 Field #####
        issue.update(fields={'customfield_1': df.iloc[row,1]})
        ##### Updates Period 2 Field #####
        issue.update(fields={'customfield_2': df.iloc[row,2]})
        ##### Updates Period 3 Field #####
        issue.update(fields={'customfield_3': df.iloc[row,3]})
        ##### Updates Period 4 Field #####
        issue.update(fields={'customfield_4': df.iloc[row,4]})
        ##### Updates Period 5 Field #####
        issue.update(fields={'customfield_5': df.iloc[row,5]})
    except:
        print(issuekey,'failed to update')
        fail += 1
        continue

##### Reports out on success of program execution #####
print(' ')
print('Upload Complete!')
print(' ')
print(row+1,'JIRAs to be updated from File')
print(row+1-fail,'JIRAs updated successfully (all fields)')
print(fail,'JIRAs failed to update (listed above if any)')
print(' ')