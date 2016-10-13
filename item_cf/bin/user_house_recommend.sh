#!/bin/bash
#author:yangyekang
#date:2016-07-04

dt=`date -d -1"days" +%Y%m%d`
JOB_NAME="user_house_recommend_yekang"

INPUT_PATH_HOUSE=${USER_HOUSE_RECOMMEND_INPUT_PATH}
OUTPUT_PATH=${USER_HOUSE_RECOMMEND_OUTPT_PATH}
HOUSE_COSINE_PATH=${HOUSE_COSINE_TOP_OUTPT_PATH}

BIN_PATH=${BIN_PATH}
HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

top_num=${TOP_NUM}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapred.job.name=${JOB_NAME}\
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.map.memory.mb=4000 \
    -D mapreduce.reduce.memory.mb=4000 \
    -D mapred.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=1 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=200 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH_HOUSE} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python user_house_recommend_map.py ${top_num}" \
    -reducer 'cat' \
    -file ${BIN_PATH}/user_house_recommend_map.py \
    -cacheFile ${HOUSE_COSINE_PATH}/part-00000#house_cosine

echo $dt
