#!/bin/bash
#author:yangyekang
#date:2016-07-04

dt=`date -d -1"days" +%Y%m%d`
JOB_NAME="recommend_optimize_yekang"

INPUT_PATH_HOUSE=${RECOMMEND_OPTIMIZE_INPUT_PATH}
OUTPUT_PATH=${RECOMMEND_OPTIMIZE_OUTPT_PATH}
USER_PREFERENCE_PATH=${USER_PREFERENCE_INPUT_PATH}
USER_FIGURE_PATH=${USER_FIGURE_OUTPT_PATH}

BIN_PATH=${BIN_PATH}
HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapred.job.name=${JOB_NAME}\
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.map.memory.mb=4000 \
    -D mapreduce.reduce.memory.mb=4000 \
    -D mapred.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=1 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=100 \
    -D mapreduce.job.reduces=100 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH_HOUSE} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python recommend_optimize_map.py" \
    -reducer "./python/bin/python recommend_optimize_reducer.py" \
    -file ${BIN_PATH}/recommend_optimize_map.py \
    -file ${BIN_PATH}/recommend_optimize_reducer.py \
    -cacheFile ${RESBLOCK_PRICE}#resblock_price \
    -cacheFile ${USER_PREFERENCE_PATH}/part-00000#user_preference \
    -cacheFile ${USER_FIGURE_PATH}/part-00000#user_figure

echo $dt
