#!/usr/bin/env bash

function method()
{
    kind=$1
    number=50
    rm -f ${kind}_result.txt

    while true
    do
        if (($number > 500))
        then
            break
        fi
        echo $kind, $number
        python run.py $kind $number >> ${kind}_result.txt
        ((number+=50))
    done
}

#method default
#method default2
method random
#method cluster
#method onlylexical
