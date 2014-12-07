#!/bin/bash
BENCHMARK_DIR="./Benchmark/"
SOLUTIONS_DIR="./solutions/"
SOLUTIONS_FILE="${SOLUTIONS_DIR}solution"
echo "" > $SOLUTIONS_FILE
sh ./compila.sh main.cpp
for i in $BENCHMARK_DIR*.txt
do
f=$(readlink -e $i)
echo "calling ./main $f \n"
start=$(date +%s%N)
OUTPUT=$(timeout 600s ./main  $f)
end=$(date +%s%N)
time_diff=$(((end-start)/1000000))
echo -e "" >> $SOLUTIONS_FILE
echo -e "$i" >> $SOLUTIONS_FILE
echo -e "TIME: $time_diff ms" >> $SOLUTIONS_FILE
echo -e $OUTPUT >> $SOLUTIONS_FILE
done

