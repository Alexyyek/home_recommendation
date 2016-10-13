#!/bin/bash
INPUT_PATH=${CLEAN_USER_VECTOR_INPUT_PATH}
OUTPUT_PATH=${CLEAN_USER_VECTOR_OUTPUT_PATH}
WEIGHT_LOWER_BOUND=${CLEAN_USER_VECTOR_WEIGHT_LOWER_BOUND}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='unified_user_vector_clean' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapredude.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=64 \
    -D mapreduce.job.reduces=20 \
    -D mapreduce.map.memory.mb=4000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -cacheArchive "${HDFS_SPIDER_FILE_PATH}#spider.txt" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python mapper.py ${WEIGHT_LOWER_BOUND}" \
    -reducer 'cat' \
    -file mapper.py
