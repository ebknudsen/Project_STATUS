import json
import os
import requests

from base import *

workflow='test_compile_cmd.yml'
wflabel='Compile Status'
repo='C2PO'
update_status(repo,workflow,wflabel)
