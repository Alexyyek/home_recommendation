#!/bin/bash
N=${TOP_N}  #最近用户数量
INPUT_PATH=${TOP_N_SIMILAR_USER_TOTAL_INPUT_PATH}
OUTPUT_PATH=${TOP_N_SIMILAR_USER_TOTAL_OUTPUT_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='top_N_similar_user_total' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=128 \
    -D mapreduce.job.reduces=50 \
    -D mapreduce.map.memory.mb=2000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper 'cat' \
    -reducer "./python/bin/python reducer.py ${N}" \
    -file reducer.py

    #-mapper './python/bin/python mapper.py' \
    #-file mapper.py \
