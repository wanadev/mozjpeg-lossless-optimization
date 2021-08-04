#!/bin/bash

##
## Lists the files to include in sdist distribution. This can be used to
## generate the MANIFEST.in contents:
##
##     scripts/generate_manifest_in.sh > MANIFEST.in
##

echo "include README.rst"
echo "include LICENSE"

echo

find mozjpeg_lossless_optimization -name "*.[hc]*" -exec echo "include" "{}" ";" \
    | grep -v "_mozjpeg_opti.c$" \
    | grep -v ".*\.\(pyc\|so\)$"

echo

find mozjpeg -type f -exec echo "include" "{}" ";" \
    | grep -v "^include mozjpeg/\(.git\|build\|doc\|java\|testimages\)" \
    | grep -v "\.\(1\|css\)$"
