#!/bin/bash
INPUT_PATH=${USER_VECTOR_INPUT_PATH}
OUTPUT_PATH=${USER_VECTOR_OUTPUT_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name="unified_user_vector" \
    -D mapreduce.job.queuename='highPriority' \
    -D mapredude.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=64 \
    -D mapreduce.job.reduces=20 \
    -D mapreduce.map.memory.mb=4000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -cacheArchive "${HDFS_HOUSE_DETAIL_PATH}#house_detail.txt" \
    -cacheArchive "${HDFS_UCID_MOBILE_PATH}#ucid_mobile.txt" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python mapper.py' \
    -reducer './python/bin/python reducer.py' \
    -file mapper.py \
    -file reducer.py

