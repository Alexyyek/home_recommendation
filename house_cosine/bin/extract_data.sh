#!/bin/bash
#Author:yangyekang
#Date:2016-07-14

JOB_NAME="extract_house_yekang"

echo ${dt}

#param map
alpha=${Alpha}
online_code=${ONLINE_CODE}
offline_code=${OFFLINE_CODE}
online_browse_weight=${ONLINE_BROWSE_WEIGHT}
online_fav_weight=${ONLINE_FAV_WEGIHT}
offline_touring_weight=${OFFLINE_TOURING_WEIGHT}
offline_contract_weight=${OFFLINE_CONTRACT_WEIGHT}
online_offline_threshold=${ONLINE_OFFLINE_THRESHOLD}
one_room_interval=${ONE_ROOM_INTERVAL}
two_room_interval=${TWO_ROOM_INTERVAL}
three_room_interval=${THREE_ROOM_INTERVAL}

PC_PATH="${PC_PATH}/*/*"
MOBILE_PATH="${MOBILE_PATH}/*/*"
ONLINE_PATH="${ONLINE_PATH}/*"
OFFLINE_PATH=${OFFLINE_PATH}
FAV_PATH="${FAV_PATH}*/*"
OUTPUT_PATH=${EXTRACT_DATA_OUTPT_PATH}

DIM_MERGE_HOUSE_DAY=${DIM_MERGE_HOUSE_DAY}

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
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=50 \
    -D mapreduce.job.reduces=50 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${PC_PATH} \
    -input ${MOBILE_PATH} \
    -input ${ONLINE_PATH} \
    -input ${OFFLINE_PATH} \
    -input ${FAV_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python extract_data_map.py ${online_browse_weight} ${online_fav_weight} ${offline_touring_weight} ${offline_contract_weight}" \
    -reducer "./python/bin/python extract_data_reducer.py ${alpha} ${online_code} ${offline_code} ${online_offline_threshold} ${one_room_interval} ${two_room_interval} ${three_room_interval}" \
    -file ${BIN_PATH}/extract_data_map.py \
    -file ${BIN_PATH}/extract_data_reducer.py \
    -cacheFile ${DIM_MERGE_HOUSE_DAY}#dim_merge_house_day \

echo $dt
