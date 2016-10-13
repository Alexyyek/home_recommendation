#!/bin/bash

dt=`date -d -1"days" +%Y%m%d`
JOB_NAME="house_user_vector"

INPUT_PATH=${HOUSE_USER_INPT_PATH}
OUTPUT_PATH=${HOUSE_USER_OUTPT_PATH}

BIN_PATH=${BIN_PATH}
HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapred.job.name=${JOB_NAME} \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.map.memory.mb=4000 \
    -D mapreduce.reduce.memory.mb=4000 \
    -D mapred.job.priority=NORMAL \
    -D stream.map.output.field.separator='\t' \
    -D stream.num.map.output.key.fields=3 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.reduces=1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper 'python house_user_vector_map.py' \
    -reducer 'python house_user_vector_reducer.py' \
    -file ${BIN_PATH}/house_user_vector_map.py \
    -file ${BIN_PATH}/house_user_vector_reducer.py

echo ${dt}
