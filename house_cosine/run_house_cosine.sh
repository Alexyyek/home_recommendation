#!/bin/bash
source "./conf/bash_conf.sh"
RUN_CUR_PATH=`pwd`
############################
##get run_time
############################
echo "RUN_DAY="${RUN_DAY}
RUN_THREE_DAY_AGO=`date -d -3"days" +%Y%m%d`


###########################
##get param for stat
##########################
CUR_RUN_TIME=${RUN_DAY}

function print_log()
##print log
#param is print string
{
        echo "====================================="
        echo "RUN LOG INFO: ${1}"
        echo "====================================="
}


#################################################
#####获取用户浏览/关注/带看/成交行为数据
###############################################
function get_extract_data
{
    sh -x "${BIN_PATH}/extract_data.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "extract_data is success !!!"
    else
        print_log "extract_data is failed !!!"
        exit 1
   fi
   cd -
}

#################################################
#####过滤稀疏数据
###############################################
function get_user_preference_filter
{
    sh -x "${BIN_PATH}/user_preference_filter.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "user_preference_filter is success !!!"
    else
        print_log "user_preference_filter is failed !!!"
        exit 1
    fi
    cd -
}

#################################################
#####生成用户向量
###############################################
function get_user_house_vector
{
    sh -x "${BIN_PATH}/user_house_vector.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "user_house_vector is success !!!"
    else
        print_log "user_house_vector is failed !!!"
        exit 1
   fi
   cd -
}

#################################################
#####生成房源向量
###############################################
function get_house_user_vector
{
    sh -x "${BIN_PATH}/house_user_vector.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "house_user_vector is success !!!"
    else
        print_log "house_user_vector is failed !!!"
        exit 1
   fi
   cd -
}

#################################################
#####房源相似度计算
###############################################
function get_house_cosine
{
    sh -x "${BIN_PATH}/house_cosine_cal.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "house_cosine_cal is success !!!"
    else
        print_log "house_cosine_cal is failed !!!"
        exit 1
   fi
   cd -
}

#################################################
#####房源相似度TOPN
###############################################
function get_house_cosine_topN
{
    sh -x "${BIN_PATH}/house_cosine_topN.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "house_cosine_topN is success !!!"
    else
        print_log "house_cosine_topN is failed !!!"
    exit 1
    fi
    ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -getmerge ${HOUSE_COSINE_TOP_OUTPT_PATH} "${DATA_PATH}/house_cosine"
    cd -
}

#################################################
#####更新redis数据库
###############################################
function update_redis
{
    cd ./data
    python ${BIN_PATH}/update_redis.py
    if [[ $? == 0 ]]
    then
        print_log "connect redis is success !!!"
    else
        print_log "connect redis is failed !!!"
    exit 1
    fi
    cd -
}

get_extract_data
get_user_preference_filter
get_user_house_vector
get_house_user_vector
get_house_cosine
get_house_cosine_topN
update_redis
