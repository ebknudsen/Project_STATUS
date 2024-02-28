import json
import os
import requests
import pathlib as pl
import subprocess as sp

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
      self.TOKEN=os.environ['GH_ACCESS_TOKEN']
    except KeyError:
      print("Need to set both GH_ACCESS_TOKEN and GH_USERNAME environment vars")
      self.username=None
      self.TOKEN=None

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
      try:
        wf_conclusion=js['workflow_runs'][0]['conclusion']
        if(wf_conclusion == 'success'):
          message='success'
          color='green'
        else:
          message=wf_conclusion
          color='red'
      except KeyError:
        message='unknown'
        color='grey'

    status=f"""{{
      "schemaVersion": 1,
      "label": "{self.wflabel}",
      "message": "{message}",
      "color": "{color}"
    }}"""
    return status

  def _write_status_file(self, status):
    need_add=False
    if not pl.Path(self.repo).exists():
      pl.Path(self.repo).mkdir()

    statusfile=f'{self.repo}/STATUS.json'
    with open(statusfile,'w') as f:
      f.write(status)
    s=sp.check_output(['git','status','--porcelain',statusfile])
    if s[1]=='?':
      sp.run({'git','add','-f',statusfile])
    sp.run(['git','commit','-q',statusfile,'-m','\"update\"'])
    sp.run(['git','push','-q'])

  def update_status(self):
    s=self._get_status()
    self._write_status_file(s)

