#!/bin/bash
#RUN_DAY=$1
RUN_MONTH='201606'
PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
INPUT_PATH="/user/hive/warehouse/log_center.db/log_dw_details_event_mobile_hour/pt=${RUN_MONTH}*/*"
OUTPUT_PATH="/user/songxin/new_unified_user_behaviour/mobile/${RUN_MONTH}"

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='get user_online_mobile data' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapredude.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=32 \
    -D mapreduce.job.reduces=10 \
    -D mapreduce.map.memory.mb=2000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python mapper.py' \
    -reducer 'cat' \
    -file mapper.py

