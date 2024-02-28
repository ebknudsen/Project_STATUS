import json
import os
import requests

from base import *

workflow='mcxtrace-run.yml'
wflabel='Compile Status'
repo='HALO_powderNunion'
r=Repo_status(repo,workflow,wflabel)
r.update_status()
