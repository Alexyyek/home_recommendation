#!/bin/bash
PART=$1
INPUT_PATH="${USER_SIMILARITY_SEG_INPUT_PATH}/part-${PART}"
OUTPUT_PATH="${USER_SIMILARITY_SEG_OUTPUT_PATH}/${PART}/"

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name="online_user_similarity_part_${PART}" \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=200 \
    -D mapreduce.job.reduces=20 \
    -D mapreduce.map.memory.mb=4000 \
    -D mapreduce.reduce.memory.mb=4000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -cacheArchive "${HDFS_CLEAN_USER_VECTOR_FILE_PATH}#user_pref_vector.txt" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python mapper.py' \
    -reducer './python/bin/python reducer.py' \
    -file mapper.py \
    -file reducer.py

