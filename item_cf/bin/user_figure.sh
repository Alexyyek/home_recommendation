#!/bin/bash

dt=`date +%Y%m%d`
JOB_NAME="user_figure_room_yekang"

INPUT_PATH=${USER_FIGURE_INPUT_PATH}
OUTPUT_PATH=${USER_FIGURE_OUTPT_PATH}

ROOM_THRESHOLD=${ROOM_THRESHOLD}
RECENT_DAYS=${RECENT_DAYS}
ONE_RECORD_MARGIN=${ONE_RECORD_MARGIN}
THRESHOLD_NINTY=${THRESHOLD_NINTY}

BIN_PATH=${BIN_PATH}
HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapred.job.name=${JOB_NAME} \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.map.memory.mb=4000 \
    -D mapreduce.reduce.memory.mb=4000 \
    -D mapred.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=1 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=50 \
    -D mapreduce.job.reduces=50 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python user_figure_map.py" \
    -reducer "./python/bin/python user_figure_reducer.py ${ROOM_THRESHOLD} ${RECENT_DAYS} ${ONE_RECORD_MARGIN} ${THRESHOLD_NINTY}" \
    -file ${BIN_PATH}/user_figure_map.py \
    -file ${BIN_PATH}/user_figure_reducer.py \
    -cacheFile ${RESBLOCK_PRICE}#resblock_price \
    -cacheFile ${SPIDER}#spider

echo ${dt}
