#!/bin/sh

sh build.sh
twine upload -r testpypi dist/*