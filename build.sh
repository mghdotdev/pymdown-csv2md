#!/bin/sh

rm -rf build dist pymdown_csv2md.egg-info;

python3 setup.py sdist bdist_wheel;
