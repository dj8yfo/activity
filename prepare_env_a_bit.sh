#!/bin/bash

set -e

pipenv install
eval ". $(pipenv --venv)/bin/activate"

./gen_proxies.sh

cd morphs-swap/
nosetests -v test/biz_page_xpath_test.py 
alembic upgrade head

