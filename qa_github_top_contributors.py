import json
import requests
import numpy as np
import pandas as pd
import time
import requests
from requests.auth import HTTPBasicAuth

credentials = json.loads(open('credentials.json').read())
authentication = HTTPBasicAuth(credentials['username'], credentials['password'])
# Read from cache if True
cacheRepos = True
cacheProjs = True
#Get all the repos in the project
repos = []

if not cacheRepos:
    for i in [1,2,3,4]:
        print(f'Grabbing repositories from page {i} of the Project')
        data = requests.get(f'https://github.com/api/v3/users/AY3308-USWMAQA/repos?per_page=100&page={i}', auth = authentication, verify=False)
        repos.extend(data.json())
        time.sleep(3)
    with open('repos.json', 'w') as f:
        print(f'Saving repos to repos.json')
        json.dump(repos, f)
else:
    print('Loading repos from cache repos.json')
    with open('repos.json', 'r') as f:
        repos = json.loads(f.read())


#Grab data of contributors for each project in the repos
projects = {}
if not cacheProjs:
    for i in repos:
        print(f'Iteration #{i} of {len(projects)}: Retrieving contributor data for the project {i.get("name")}')
        data = requests.get(f'https://github.com/api/v3/repos/AY3308-USWMAQA/{i.get("name")}/contributors', auth = authentication, verify=False)
        #Add the project to the projects dict
        try:
            projects[i.get("name")]=data.json()
            with open('projects.json', 'w') as f:
                json.dump(projects, f)
        except ValueError:
                print(f'Unable to get contributor data for {i.get("name")}')
    time.sleep(3)
else:
    print('Loading projects from Cache')
    with open('projects.json', 'r') as f:
        projects = json.loads(f.read())

#Go through each repo, get the login user and the number of contributions. Add it to a map.
contribs = {}
for j in projects.keys():
    for k in projects.get(j):
        if not k.get('login') in contribs:
            contribs[k.get('login')]=k.get('contributions')
        else:
            contribs[k.get('login')]+=k.get('contributions')

#Convert the map to a list. This makes displaying it in the UI Grid much easier
contribsList = []
for key, value in contribs.items():
    entry = {'username': key, 'commits': value}
    contribsList.append(entry)
with open('contribs.js', 'w') as f:
    json.dump(contribsList, f)

        
