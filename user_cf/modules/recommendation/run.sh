#!/bin/bash
INPUT_PATH=${RECOMMENDATION_INPUT_PATH}
OUTPUT_PATH=${RECOMMENDATION_OUTPUT_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='online_recommendation' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=32 \
    -D mapreduce.job.reduces=10 \
    -D mapreduce.map.memory.mb=6000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -cacheArchive "${HDFS_USER_TOURING_SET_FILE_PATH}#user_touring.txt" \
    -cacheArchive "${HDFS_CLEAN_USER_VECTOR_FILE_PATH}#user_pref_vector.txt" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python mapper.py ${RECOMMENDATION_NO}" \
    -reducer 'cat' \
    -file mapper.py \

