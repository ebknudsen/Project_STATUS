import json
import os
import requests
import pathlib as pl

class Repo_status:
  def __init__(self,repo='repository',workflow='status.yml', wflabel=None):
    self.repo=repo
    self.workflow=workflow
    if wflabel is None:
      self.wflabel=pl.Path(workflow).stem
    else:
      self.wflabel=wflabel

    try:
      self.username=os.environ['GH_USERNAME']
      TOKEN=os.environ['GH_ACCESS_TOKEN']
    except KeyError:
      print("Need to set both GH_ACCESS_TOKEN and GH_USERNAME environment vars")

  def _get_status(self):
    if (self.TOKEN is None or self.username is None):
      message='unknown'
      color='gray'
    else:
      headers={'Accept': 'application/vnd.github+json', 'Authorization': f'Bearer {self.TOKEN}', "X-GitHub-Api-Version": "2022-11-28"}

      #get the workflow result
      r=requests.get(f'https://api.github.com/repos/{self.username}/{self.repo}/actions/workflows/{self.workflow}/runs',headers=headers)
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
      "label": "{self.wflabel}",
      "message": "{message}",
      "color": "{color}"
    }}"""
    return status

  def _write_status_file(self):
    if not pl.Path(self.repo).exists():
      pl.Path(self.repo).mkdir()
      need_add=True

    statusfile=f'{self.repo}/STATUS.json'
    with open(statusfile,'w') as f:
      f.write(status)
    if need_add:
      os.system(f'git add -f {statusfile}')
    os.system(f'git commit -q {statusfile} -m \"update\"')
    os.system('git push -q')

  def update_status(self):
    s=self._get_status()
    self._write_status_file()

