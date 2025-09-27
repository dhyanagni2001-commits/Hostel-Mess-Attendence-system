#!/usr/bin/env bash

PROJECT_PATH=`pwd`
VENV_PATH=$PROJECT_PATH/pyvenv

python -m venv $VENV_PATH
. $VENV_PATH/Scripts/activate

$VENV_PATH/Scripts/python.exe -m pip install --upgrade pip

pip install -r $PROJECT_PATH/requirements.txt