#!/bin/bash
if [ $# -eq 0 ];
then
   export RUN_DAY=`date -d"-1 day" +%Y%m%d`
else
   export RUN_DAY=$1
fi
export DEAD_DAY=`date -d"${RUN_DAY} -1 day" +%Y%m%d`
export RUN_MONTH=`date -d"${RUN_DAY}" +%Y%m`

#basic config
export CITY_ID='110000'
export BIZ_TYPE='200200000001'
export BEGIN_DATE='20140601'   #系统输入截取的初始时间
export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
export HADOOP_HOME='/home/work/bin/hadoop'

export LOCAL_HOUSE_DETAIL_PATH="./data/house_detail/${RUN_DAY}.txt"
export HDFS_HOUSE_DETAIL_PATH="/user/songxin/tools/house_detail/${RUN_DAY}.txt"
export LOCAL_UCID_MOBILE_PATH="./data/ucid_mobile/${RUN_DAY}.txt"
export HDFS_UCID_MOBILE_PATH="/user/songxin/tools/ucid_mobile/${RUN_DAY}.txt"
export LOCAL_USER_FAV_PATH="./data/user_fav/${RUN_DAY}.txt"
export HDFS_USER_FAV_PATH="/user/songxin/new_unified_user_behaviour/user_fav/${RUN_DAY}/${RUN_DAY}.txt"
export LOCAL_USER_TOURING_PATH="./data/user_touring/${RUN_DAY}.txt"
export HDFS_USER_TOURING_PATH="/user/songxin/tools/user_touring/${RUN_DAY}.txt"
export LOCAL_SPIDER_FILE_PATH="./data/spider/${RUN_DAY}.txt"
export HDFS_SPIDER_FILE_PATH="/user/songxin/tools/spider/spider.txt"

#用户线下行为数据
export USER_OFFLINE_INPUT_PATH="/user/bigdata/profiling/customer_${RUN_DAY}/"
export USER_OFFLINE_OUTPUT_PATH="/user/songxin/new_unified_user_behaviour/offline_data/${RUN_DAY}"

#用户线上行为数据
export USER_ONLINE_UAL_INPUT_PATH="/user/hive/warehouse/search.db/dw_log_www_all_item_access/pt=${RUN_MONTH}*/*"
export USER_ONLINE_UAL_OUTPUT_PATH="/user/songxin/new_unified_user_behaviour/ual_behaviour/${RUN_MONTH}"

#export USER_ONLINE_PC_INPUT_PATH="/user/hive/warehouse/log_center.db/log_dw_details_pc_hour/pt=${RUN_MONTH}*/*"
#export USER_ONLINE_PC_OUTPUT_PATH="/user/songxin/unified_user_behaviour/pc/${RUN_MONTH}"
#export USER_ONLINE_MOBILE_INPUT_PATH="/user/hive/warehouse/log_center.db/log_dw_details_event_mobile_hour/pt=${RUN_MONTH}*/*"
#export USER_ONLINE_MOBILE_OUTPUT_PATH="/user/songxin/unified_user_behaviour/mobile/${RUN_MONTH}"

#user_vector
export USER_VECTOR_INPUT_PATH="/user/songxin/unified_user_behaviour/*/*/"
export USER_VECTOR_OUTPUT_PATH="/user/songxin/unified_recommendation/user_pref_vector/${RUN_DAY}/"

#user_vector_clean
export CLEAN_USER_VECTOR_INPUT_PATH=${USER_VECTOR_OUTPUT_PATH}
export CLEAN_USER_VECTOR_OUTPUT_PATH="/user/songxin/unified_recommendation/user_pref_vector_clean/${RUN_DAY}/"
export CLEAN_USER_VECTOR_WEIGHT_LOWER_BOUND=0.01
export LOCAL_CLEAN_USER_VECTOR_FILE_PATH="./data/user_vector_clean/${RUN_DAY}.txt"
export HDFS_CLEAN_USER_VECTOR_FILE_PATH="/user/songxin/tools/user_vector_clean/${RUN_DAY}.txt"

#inverse_index
export INVERSE_INDEX_INPUT_PATH=${CLEAN_USER_VECTOR_OUTPUT_PATH}
export INVERSE_INDEX_OUTPUT_PATH="/user/songxin/unified_recommendation/resblock_inverse_index/${RUN_DAY}/"

#user_similarity_seg
export USER_SIMILARITY_SEG_INPUT_PATH="/user/songxin/unified_recommendation/resblock_inverse_index/${RUN_DAY}"
export USER_SIMILARITY_SEG_OUTPUT_PATH="/user/songxin/unified_recommendation/user_similarity_segs/${RUN_DAY}"

#user_similarity_merge
export USER_SIMILARITY_MERGE_INPUT_PATH="/user/songxin/unified_recommendation/user_similarity_segs/${RUN_DAY}"
export USER_SIMILARITY_MERGE_OUTPUT_PATH="/user/songxin/unified_recommendation/user_similarity_merge/${RUN_DAY}"

#user_similarity_total
#export USER_SIMILARITY_TOTAL_INPUT_PATH="${USER_SIMILARITY_MERGE_OUTPUT_PATH}/*/*"
export USER_SIMILARITY_TOTAL_INPUT_PATH="${USER_SIMILARITY_SEG_OUTPUT_PATH}/*/*"
export USER_SIMILARITY_TOTAL_OUTPUT_PATH="/user/songxin/unified_recommendation/user_similarity_total/${RUN_DAY}/"

#top_N_similar_user_seg
export TOP_N_SIMILAR_USER_SEG_INPUT_PATH=${USER_SIMILARITY_TOTAL_OUTPUT_PATH}
export TOP_N_SIMILAR_USER_SEG_OUTPUT_PATH="/user/songxin/unified_recommendation/top_50_similar_user_seg/${RUN_DAY}/"
export TOP_N=50

#top_N_similar_user
#export TOP_N_SIMILAR_USER_INPUT_PATH=${USER_SIMILARITY_TOTAL_OUTPUT_PATH}
export TOP_N_SIMILAR_USER_TOTAL_INPUT_PATH="${TOP_N_SIMILAR_USER_SEG_OUTPUT_PATH}/*/*"
export TOP_N_SIMILAR_USER_TOTAL_OUTPUT_PATH="/user/songxin/unified_recommendation/top_50_similar_user_total/${RUN_DAY}/"

#user_touring
export USER_TOURING_INPUT_PATH=${USER_OFFLINE_OUTPUT_PATH}
export USER_TOURING_OUTPUT_PATH="/user/songxin/unified_recommendation/user_touring/${RUN_DAY}"
export LOCAL_USER_TOURING_SET_FILE_PATH="./data/user_touring_set/${RUN_DAY}.txt"
export HDFS_USER_TOURING_SET_FILE_PATH="/user/songxin/tools/user_touring/${RUN_DAY}.txt"

#recommendation
export RECOMMENDATION_INPUT_PATH=${TOP_N_SIMILAR_USER_TOTAL_OUTPUT_PATH}
export RECOMMENDATION_OUTPUT_PATH="/user/songxin/unified_recommendation/recommendation_result/${RUN_DAY}"
export RECOMMENDATION_NO=50
