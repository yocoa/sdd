#!/usr/bin/env bash

number=10
rm -f result.txt

while true
do
    if (($number > 100))
    then
        break
    fi
    echo default, $number
    python main.py default $number >> result.txt
    ((number+=10))
done

number=100
while true
do
    if (($number > 2000))
    then
        break
    fi
    echo default, $number
    python main.py default $number >> result.txt
    ((number+=100))
done
