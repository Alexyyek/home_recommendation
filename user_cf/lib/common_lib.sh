#!/bin/bash
function prepare_data
{
    hive -e "select house_pkid, total_prices, build_area, room_cnt, parlor_cnt, cookroom_cnt, toilet_cnt, balcony_cnt, resblock_id, resblock_name, district_name, bizcircle_name from data_center.dim_merge_house_day where pt='${RUN_DAY}000000' and biz_type='${BIZ_TYPE}' and city_id='${CITY_ID}';" > ${LOCAL_HOUSE_DETAIL_PATH}
    hive -e "select id, mobile from ods.ods_uc_user_da where pt='${RUN_DAY}000000';" > ${LOCAL_UCID_MOBILE_PATH}
    hive -e "select uc_id, fav_time, fav_object_id, fav_object_type from data_center.dim_user_fav_day where pt='${RUN_DAY}000000' and fav_time>='2014-06-01' and (fav_object_type='ershoufang' or fav_object_type='resblock');" > ${LOCAL_USER_FAV_PATH}

    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_HOUSE_DETAIL_PATH} ${HDFS_HOUSE_DETAIL_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_UCID_MOBILE_PATH} ${HDFS_UCID_MOBILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_USER_FAV_PATH} ${HDFS_USER_FAV_PATH}
}


function print_log()
##print log
#param is print string
{
    echo "====================================="
    echo "RUN LOG INFO: ${1}"
    echo "====================================="
}

