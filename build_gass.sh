#!/bin/sh
. ./files.sh

for i in "${FILES[@]}"; do
    python pak.py gass/$i
done

