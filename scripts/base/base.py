def _get_status(repo,workflow,wflabel):
  username=os.environ['GH_USERNAME']
  TOKEN=os.environ['GH_ACCESS_TOKEN']
  if (TOKEN is None or username is None):
    print("Need to set both GH_ACCESS_TOKEN and GH_USERNAME environment vars")
    message='unknown'
    color='gray'
  else:
    headers={'Accept': 'application/vnd.github+json', 'Authorization': f'Bearer {TOKEN}', "X-GitHub-Api-Version": "2022-11-28"}

    #get the workflow result
    r=requests.get(f'https://api.github.com/repos/{username}/{repo}/actions/workflows/{workflow}/runs',headers=headers)
    js=r.json()
    #check the status - was the workflow run a success or no?
    wf_conclusion=js['workflow_runs'][0]['conclusion']
    if(wf_conclusion == 'success'):
      message='success'
      color='green'
    else:
      message=wf_conclusion
      color='red'

  status=f"""{{
    "schemaVersion": 1,
    "label": "{wflabel}",
    "message": "{message}",
    "color": "{color}"
  }}"""
  return status

def _write_status_file(repo,status):
  statusfile=f'{repo}/STATUS.json'
  with open(statusfile,'w') as f:
    f.write(status)
  os.system(f'git commit {statusfile} -m \"update\"')
  os.system('git push -q')

def update_status(repo,workflow,wflabel):
  s=_get_status(repo,workflow,wflabel)
  _write_status_file(repo,s)

