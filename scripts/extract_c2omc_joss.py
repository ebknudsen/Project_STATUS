import json
import os
import requests

from base import *

workflow='draft-pdf.yml'
wflabel='Compile Status'
repo='c2omc_joss'
r=Repo_status(repo,workflow,wflabel)
r.update_status()
