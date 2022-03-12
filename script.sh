#!/bin/bash

clear
rm data.csv 
rm out.txt 
rm circuit.json 
rm *.png 
rm analysis.py

cp ../analysis.py .
python analysis.py 
