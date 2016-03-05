#!/usr/bin/env bash

readonly WORKSPACE=$(pwd)
readonly services=(\
    BgpBase\
    VisualSimilarity\
    AccessingRelation\
)
readonly opts=("import")

function nothing()
{
    echo "do nothing... exit"
    exit 0;
}

function adapter()
{
    if [[ ${opts[@]} =~ "$1" ]]
    then
        opt="$1"
        path="$2"
    else
        echo "Usage: ./adapter.sh [import/export] directory"
        nothing
    fi

    case "$opt" in
        "import" )
            if [ -d "$path" ]
            then
                for ((i=0;i<${#services[@]};i++))
                do  
                    s=${services[$i]}
                    mkdir -p "$WORKSPACE/services/$s/data"
                    echo "cp $path/${s}_data -> $WORKSPACE/services/$s/data/train"
                    cp $path/${s}_data $WORKSPACE/services/$s/data/train
                done
            else
                nothing
            fi
        ;;
        * )
            nothing
        ;;
    esac
}

# Main entrance
adapter "$1" "$2"
