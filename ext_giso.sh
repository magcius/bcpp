#!/bin/sh
. ./files.sh

cd gext
7z x ../giso/orig_game.iso
cd ..

for i in "${FILES[@]}"; do
    cp gext/PSP_GAME/USRDIR/$i gass/$i
    chmod -x+w gass/$i
done
