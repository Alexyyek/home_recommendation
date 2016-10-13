#!/bin/bash
source ./conf/conf.sh
function prepare_tools_data
{
    TOOL_DATA_DEAD_DAY=`date -d"-3 day" +%Y%m%d`

    LOCAL_DIR_PATH=`dirname ${LOCAL_HOUSE_DETAIL_PATH}`
    HDFS_DIR_PATH=`dirname ${HDFS_HOUSE_DETAIL_PATH}`
    hive -e "select house_pkid, total_prices, build_area, room_cnt, parlor_cnt, cookroom_cnt, toilet_cnt, balcony_cnt, resblock_id, resblock_name, district_name, bizcircle_name from data_center.dim_merge_house_day where pt='${RUN_DAY}000000' and biz_type='${BIZ_TYPE}' and city_id='${CITY_ID}';" > ${LOCAL_HOUSE_DETAIL_PATH}
    rm ${LOCAL_DIR_PATH}/${TOOL_DATA_DEAD_DAY}.txt
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_HOUSE_DETAIL_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_HOUSE_DETAIL_PATH} ${HDFS_HOUSE_DETAIL_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_DIR_PATH}/${TOOL_DATA_DEAD_DAY}.txt

    LOCAL_DIR_PATH=`dirname ${LOCAL_UCID_MOBILE_PATH}`
    HDFS_DIR_PATH=`dirname ${HDFS_UCID_MOBILE_PATH}`
    hive -e "select id, mobile from ods.ods_uc_user_da where pt='${RUN_DAY}000000';" > ${LOCAL_UCID_MOBILE_PATH}
    rm ${LOCAL_DIR_PATH}/${TOOL_DATA_DEAD_DAY}.txt
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_UCID_MOBILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_UCID_MOBILE_PATH} ${HDFS_UCID_MOBILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_DIR_PATH}/${TOOL_DATA_DEAD_DAY}.txt

    LOCAL_DIR_PATH=`dirname ${LOCAL_USER_FAV_PATH}`
    HDFS_DIR_PATH=`dirname ${HDFS_USER_FAV_PATH}`
#    hive -e "select uc_id, fav_time, fav_object_id, fav_object_type from data_center.dim_user_fav_day where pt='${RUN_DAY}000000' and fav_time>='2014-06-01' and (fav_object_type='ershoufang' or fav_object_type='resblock');" > ${LOCAL_USER_FAV_PATH}
    SQL='select user_id, ctime, favorite_condition, favorite_type from lianjia.lianjia_user_favorite where bit_status="1" and (favorite_type="ershoufang" or favorite_type="resblock");'
    mysql -h 172.16.6.183 -P 6521 -uphpmyadmin -p'w2e#-s1f!^)()' -N -e "${SQL}" > ${LOCAL_USER_FAV_PATH}
    rm ${LOCAL_DIR_PATH}/${TOOL_DATA_DEAD_DAY}.txt
    ${HADOOP_HOME}/bin/hadoop fs -mkdir ${HDFS_DIR_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_USER_FAV_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_USER_FAV_PATH} ${HDFS_USER_FAV_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -rm -r ${HDFS_DIR_PATH}/../${TOOL_DATA_DEAD_DAY}
}

function prepare_user_behaviour_data
{
    HDFS_DIR_PATH=`dirname ${USER_OFFLINE_OUTPUT_PATH}`
    ${HADOOP_HOME}/bin/hadoop fs -rm -r ${HDFS_DIR_PATH}/${DEAD_DAY}
    cd ./get_data_new/offline_user_data
    sh -x run.sh
    cd -

    cd ./get_data_new/online_user_data
    sh -x run.sh
    cd -
}

function prepare_spider_data
{
    SQL='select phone from data_mining.house_see_spider where phone!="NULL";'
    rm ${LOCAL_SPIDER_FILE_PATH}/../${DEAD_DAY}.txt
    hive -e "${SQL}" > ${LOCAL_SPIDER_FILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_SPIDER_FILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_SPIDER_FILE_PATH} ${HDFS_SPIDER_FILE_PATH}
}

prepare_tools_data
prepare_user_behaviour_data
prepare_spider_data

