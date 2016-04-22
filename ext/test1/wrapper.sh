#!/usr/bin/env bash

function method()
{
    small_or_large=$1
    kind=$2
    number=50
    rm -f ${kind}_result.txt

    while true
    do
        if (($number > 500))
        then
            break
        fi
        echo $kind, $number
        python run.py $small_or_large $kind $number >> ${kind}_result.txt
        ((number+=50))
    done
}

method small lexical
#method default2
#method random
#method cluster
#method onlylexical
#method cluster_new
