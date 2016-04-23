#!/usr/bin/env bash

function method()
{
    small_or_large=$1
    kind=$2
    number=50
    rm -f ${small_or_large}_${kind}_result.txt

    while true
    do
        if (($number > 500))
        then
            break
        fi
        echo $kind, $number
        python run.py $small_or_large $kind $number >> ${small_or_large}_${kind}_result.txt
        ((number+=50))
    done
}
#method large lexical
#method large topk
#method large topk2
#method large kmeans2

method small topk2
method small kmeans2
