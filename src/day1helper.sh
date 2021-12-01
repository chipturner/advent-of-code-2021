#!/bin/bash

perl -lane '++$c if $F[0] > $x; $x = $F[0]; END { print $c - 1}'
