#!/bin/bash

dt=`date +%Y%m%d`
JOB_NAME="house_cosine_topN_yekang"

topN=${TOPN}
INPUT_PATH=${HOUSE_COSINE_TOP_INPUT_PATH}
OUTPUT_PATH=${HOUSE_COSINE_TOP_OUTPT_PATH}

BIN_PATH=${BIN_PATH}
HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapred.job.name=${JOB_NAME} \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.reduce.memory.mb=4000 \
    -D mapred.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=1 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=10 \
    -D mapreduce.job.reduces=1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python house_cosine_topN_map.py' \
    -reducer "./python/bin/python house_cosine_topN_reducer.py ${topN}" \
    -file ${BIN_PATH}/house_cosine_topN_map.py \
    -file ${BIN_PATH}/house_cosine_topN_reducer.py

echo ${dt}
