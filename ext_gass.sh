#!/bin/sh
. ./files.sh

for i in "${FILES[@]}"; do
    python ext.py gass/$i
done
