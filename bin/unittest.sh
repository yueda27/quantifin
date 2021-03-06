#!/bin/bash
echo $1
if [[ $1 == "coverage" ]]; then
    coverage run --omit '*/virtualenvs/*' -m unittest discover ./
    coverage report -m
else
    python -m unittest discover ./
fi