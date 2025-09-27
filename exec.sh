#!/usr/bin/env bash

PROJECT_PATH=`pwd`
cd $PROJECT_PATH

rm -rf static/data
pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" app.py