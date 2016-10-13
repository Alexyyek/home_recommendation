#!/bin/bash
for((i=0;i<10;++i))
do
    part=`printf "%05d\n" ${i}`
    sh -x task.sh ${part}
done
