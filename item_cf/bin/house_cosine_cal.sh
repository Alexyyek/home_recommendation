#!/bin/bash

dt=`date -d -1"days" +%Y%m%d`
JOB_NAME="house_cosine_cal_yekang"

INPUT_PATH=${HOUSE_COSINE_INPUT_PATH}
OUTPUT_PATH=${HOUSE_COSINE_OUTPT_PATH}
HOUSE_USER_VECTOR=${HOUSE_USER_OUTPT_PATH}

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
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=100 \
    -D mapreduce.job.reduces=100 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python house_cosine_cal_map.py' \
    -reducer './python/bin/python house_cosine_cal_reducer.py' \
    -file ${BIN_PATH}/house_cosine_cal_map.py \
    -file ${BIN_PATH}/house_cosine_cal_reducer.py \
    -cacheFile ${HOUSE_USER_VECTOR}/part-00000#house_user_vector

echo ${dt}
