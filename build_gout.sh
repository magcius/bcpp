#!/bin/sh
cd gext
genisoimage -input-charset iso8859-1 -l -allow-lowercase -omit-version-number -o ../gout/game.iso .
