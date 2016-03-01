#!/usr/bin/env bash

cd lib

Modules=(\
    LexicalFeature\
    NetworkFeature\
)

num=1
for module in ${Modules[@]}
do
  echo "[$num] Testing $module"
  cd "$module" && python -m unittest "$module"_test && cd >/dev/null -
  if [ $? != 0 ]
  then
    exit 1
  fi

  num=$((num+1))
  echo ""
done

