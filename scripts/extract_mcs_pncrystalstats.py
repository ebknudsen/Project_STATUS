import json
import os
import requests
import subprocess
import pathlib
import sys

repobase=pathlib.Path(sys.argv[0]).parent / '..'

username=os.environ['GH_USERNAME']
TOKEN=os.environ['GH_ACCESS_TOKEN']
if (TOKEN is None or username is None):
  print("Need to set both GH_ACCESS_TOKEN and GH_USERNAME environment vars")

headers={'Accept': 'application/vnd.github+json', 'Authorization': f'Bearer {TOKEN}', 'X-GitHub-Api-Version': '2022-11-28'}

workflow='mcstas-3-run.yml'
wflabel='McStas-3.0_compile'
repo='McStas_perfect_neutron_crystal'
#get the workflow result
url=f'https://api.github.com/repos/{username}/{repo}/actions/workflows/{workflow}/runs'
r=requests.get(url,headers=headers)
js=r.json()
#was the workflow succesful or not
# -> write the status in a string
if(js['workflow_runs'][0]['conclusion'] == 'success'):
  status=f"""{{
  "schemaVersion": 1,
  "label": "{wflabel}",
  "message": "success",
  "color": "green"
}}"""
else:
  status=f"""{{
  "schemaVersion": 1,
  "label": "{wflabel}",
  "message": "failed",
  "color": "red"
}}"""

statusfile=repobase / f'{repo}/STATUS.json'
before=subprocess.check_output(['md5sum',str(statusfile)]) 
with open(statusfile,'w') as f:
  f.write(status)
after=subprocess.check_output(['md5sum',str(statusfile)]) 
if (after != before):
  os.system(f'git commit {statusfile} -m \"status change\"')
  os.system('git push') 
