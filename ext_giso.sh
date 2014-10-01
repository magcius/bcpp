#!/bin/sh
. ./files.sh

cd gext
7z x ../giso/orig_game.iso

for i in "${FILES[@]}"; do
    chmod -x +w $i
done
