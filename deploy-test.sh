#!/bin/sh

source .env

sh build.sh
pipenv run twine upload -u $TWINE_USERNAME -p $TWINE_PASSWORD -r testpypi dist/*