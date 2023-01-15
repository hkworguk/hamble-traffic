#!/bin/sh  
while true  
do  
  python utils/Data.py
  python utils/Graphs.py
  git add data/
  git add graphs/
  git commit -m "Auto backup"
  git push
  echo "Sleeping for a bit..."
  sleep 500
done
