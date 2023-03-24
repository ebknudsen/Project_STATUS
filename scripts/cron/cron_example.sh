#!/usr/bin/env bash

#get the github access token module
ml gh_access

cd Repos/Project_STATUS
for script in `ls scripts`; do
  if [ -d $script ]; then 
    continue
  elif [ -x $script ]; then
    scripts/${script}
  else
    python scripts/${script}
  fi
done

#update all the status tokens and push it upstream such that other projects can have access
git commit -a
git push

#unload the access token module
ml -gh_access
