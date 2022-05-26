#!/bin/bash

rm data.csv 
rm out.txt 
rm circuit.json 
rm *.png 
rm analysis.py
clear

cp ../analysis.py .
python analysis.py 
