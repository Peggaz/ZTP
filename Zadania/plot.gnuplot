#!/usr/bin/gnuplot

set terminal pngcairo size 1024,768

set output 'plot.png'

maks = 300

slow = 3

set xrange [1:slow]

set yrange [1:maks]

set datafile separator ","

plot '../wyniki/Lista.csv' using 1:3 pt 7 ps 1 title 'csv'