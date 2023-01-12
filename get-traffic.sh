#!/bin/sh  
while true  
do  
  python Utils.py
  python Visuals.py
  git add data/
  git add graphs/
  git commit -m "Auto backup"
  git push
  echo "Sleeping for a bit..."
  sleep 299
done
