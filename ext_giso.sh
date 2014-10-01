#!/bin/sh
. ./files.sh

7z x giso/orig_game.iso -o gass/

for i in "${FILES[@]}"; do
    chmod -x +w gass/$i
done
