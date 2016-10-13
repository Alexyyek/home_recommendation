#!/bin/bash
INPUT_PATH=${USER_OFFLINE_INPUT_PATH}
OUTPUT_PATH=${USER_OFFLINE_OUTPUT_PATH}
echo ${INPUT_PATH}
echo ${OUTPUT_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
${HADOOP_HOME}/bin/hadoop  jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name="offline_data_extraction_${RUN_DAY}" \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=64 \
    -D mapreduce.job.reduces=5 \
    -D mapreduce.map.memory.mb=2000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python mapper.py ${BEGIN_DATE}" \
    -reducer "cat" \
    -file mapper.py

