#!/bin/bash

overwrite=false

cs=false
t1=true
t2=true
t4=true

while getopts atoc124 flag
do
    case "${flag}" in
        a) 
            cs=true
            t1=true
            t2=true
            t4=true
            ;;
        t) 
            cs=false
            t1=true
            t2=true
            t4=true
            ;;
        c)
            cs=true
            t1=false
            t2=false
            t4=false
            ;;
        o)
            overwrite=true
            ;;
        1)
            cs=false
            t1=true
            t2=false
            t4=false
            ;;
        2)
            cs=false
            t1=false
            t2=true
            t4=false
            ;;
        4)
            cs=false
            t1=false
            t2=false
            t4=true
            ;;
    esac
done

if [ "$overwrite" = true ]
then
    if [ "$cs" = true ]
    then
        python3 experiments-jair/experiments.py cs True
    fi

    if [ "$t1" = true ]
    then
        python3 experiments-jair/experiments.py t1 True
    fi

    if [ "$t2" = true ]
    then
        python3 experiments-jair/experiments.py t2 True
    fi

    if [ "$t4" = true ]
    then
        python3 experiments-jair/experiments.py t4 True
    fi

else
    if [ "$cs" = true ]
    then
        python3 experiments-jair/experiments.py cs False
    fi

    if [ "$t1" = true ]
    then
        python3 experiments-jair/experiments.py t1 False
    fi

    if [ "$t2" = true ]
    then
        python3 experiments-jair/experiments.py t2 False
    fi

    if [ "$t4" = true ]
    then
        python3 experiments-jair/experiments.py t4 False
    fi

fi