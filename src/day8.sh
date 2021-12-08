#!/bin/sh

# basically do this

cat src/input8.txt | cut -d'|' -f2  | tr ' ' '\n' | perl -lane 'print length($F[0])' | sun

# answer is the sum of lines for 1 4 7 8
