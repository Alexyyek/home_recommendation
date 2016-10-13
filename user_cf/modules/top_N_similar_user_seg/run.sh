#!/bin/bash
N=${TOP_N}  #最近用户数量
INPUT_PATH=${TOP_N_SIMILAR_USER_SEG_INPUT_PATH}
OUTPUT_PATH=${TOP_N_SIMILAR_USER_SEG_OUTPUT_PATH}

for((i=0;i<5;++i))
do
    input="${INPUT_PATH}part-000${i}*"
    output="${OUTPUT_PATH}PART_${i}/"
    sh -x task.sh ${input} ${output} ${N}
done
