#!/usr/bin/env bash

#get the github access token module
ml gh_access

cd repos/Project_STATUS/
for script in `ls scripts`; do
  fp=scripts/${script}
  if [ -d $fp ]; then 
    continue
  elif [ -x $fp ]; then
    ${fp}
  else
    python ${fp}
  fi
done

#update all the status tokens and push it upstream such that other projects can have access
git commit -a -m"update status tokens"
git push

#unload the access token module
ml -gh_access
