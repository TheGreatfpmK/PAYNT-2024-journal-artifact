#!/bin/bash

overwrite=false

cs=false
t2=true
t4=true

while getopts ato24 flag
do
    case "${flag}" in
        a) 
            cs=true
            t2=true
            t4=true
            ;;
        t) 
            cs=false
            t2=true
            t4=true
            ;;
        o)
            overwrite=true
            ;;
        2)
            cs=false
            t2=true
            t4=false
            ;;
        4)
            cs=false
            t2=false
            t4=true
            ;;
    esac
done

if [ "$overwrite" = true ]
then
    if [ "$cs" = true ]
    then
        python3 experiments-tac/experiments.py cs True
    fi
    if [ "$t2" = true ]
    then
        python3 experiments-tac/experiments.py t2 True
    fi
    if [ "$t4" = true ]
    then
        python3 experiments-tac/experiments.py t4 True
    fi
else
        if [ "$cs" = true ]
    then
        python3 experiments-tac/experiments.py cs False
    fi
    if [ "$t2" = true ]
    then
        python3 experiments-tac/experiments.py t2 False
    fi
    if [ "$t4" = true ]
    then
        python3 experiments-tac/experiments.py t4 False
    fi
fi