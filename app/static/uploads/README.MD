## Install virtual environmet
cd wbs-bim-revit
python -m venv venv

## run venv
venv\Scripts\activate

## install library
pip install -r requirements.txt

## import table
create database name: db_wbs_bim_revit
import file db_wbs_bim_revit.sql

## running
flask run

## testing
open postman
import file flask-wbs-bim-revit.postman_collection.json