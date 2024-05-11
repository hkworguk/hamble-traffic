#!/bin/bash

counter=0

while true  
do
  echo "Running Applications"
  python utils/Data.py
  python utils/Graphs.py
  # if [ $counter -gt 100 ]; then
  #   echo "Comitting changes"
  #   git add data/
  #   git add graphs/
  #   git commit -m "Auto backup"
  #   git push
  #   counter=0
  # fi;
  # ((counter++))
  echo "Sleeping for a bit..."
  sleep 300
done
