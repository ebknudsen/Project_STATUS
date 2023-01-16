import json
import os
import requests

username=os.environ['GH_USERNAME']
TOKEN=os.environ['GH_ACCESS_TOKEN']
if (TOKEN is None or username is None):
  print("Need to set both GH_ACCESS_TOKEN and GH_USERNAME environment vars")

headers={'Accept': 'application/vnd.github+json', 'Authorization': f'Bearer {TOKEN}', "X-GitHub-Api-Version": "2022-11-28"}

workflow='mcstas-3.0_compile.yml'
repo='McStas_perfect_neutron_crystal'
#get the workflow result
r=requests.get(f'https://api.github.com/repos/{username}/{repo}/actions/workflows/{workflow}/runs',headers=headers)
js=r.json()
#was the work
if(js['workflow_runs'][0]['conclusion'] == 'success'):
  status="""{
  'schemaVersion': 1,
  'label': 'TEST',
  'message': 'success',
  'color': 'green'
}"""
else:
  status="""{
  'schemaVersion': 1,
  'label': 'TEST',
  'message': 'failed',
  'color': 'red'
}"""

statusfile=f'{repo}/STATUS.json'
with open(statusfile,'w') as f:
  f.write(status)
os.system(f'git commit {statusfile} -m \"update\"')
os.system('git push') 
