#!/bin/sh
. ./files.sh

for i in "${FILES[@]}"; do
    cp gass/$i gext/PSP_GAME/USRDIR/$i
done
