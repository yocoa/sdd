#!/usr/bin/env bash

function default_method0()
{
    rm -f default_result0.txt
    python main.py default 0 >> default_result0.txt
}

function default_method()
{
    number=30
    rm -f default_result.txt

    while true
    do
        if (($number > 600))
        then
            break
        fi
        echo default, $number
        python main.py default $number >> default_result.txt
        ((number+=30))
    done
}

function random_method()
{
    number=30
    rm -f random_result.txt

    while true
    do
        if (($number > 600))
        then
            break
        fi
        echo random, $number
        python main.py random $number >> random_result.txt
        ((number+=30))
    done
}

function random_method2()
{
    number=30
    rm -f random_result2.txt

    while true
    do
        if (($number > 600))
        then
            break
        fi
        echo random2, $number
        python main.py random2 $number >> random_result2.txt
        ((number+=30))
    done
}

default_method0
#default_method
#random_method
#random_method2
