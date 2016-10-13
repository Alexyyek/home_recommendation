#!/bin/bash
INPUT_PATH=${USER_SIMILARITY_TOTAL_INPUT_PATH}
OUTPUT_PATH=${USER_SIMILARITY_TOTAL_OUTPUT_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='USER_SIMILARITY_AGGREGATE' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=64 \
    -D mapreduce.job.reduces=50 \
    -D mapreduce.map.memory.mb=2000 \
    -D mapreduce.reduce.memory.mb=5000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -cacheArchive "${HDFS_CLEAN_USER_VECTOR_FILE_PATH}#user_pref_vector.txt" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper 'cat' \
    -reducer './python/bin/python reducer.py' \
    -file reducer.py

