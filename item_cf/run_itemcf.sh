#!/bin/bash
source "./conf/bash_conf.sh"
RUN_CUR_PATH=`pwd`
############################
##get run_time
############################
echo "RUN_DAY="${RUN_DAY}


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
   ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -getmerge ${USER_PREFERENCE_INPUT_PATH} "${DATA_PATH}/user_preference"
   ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -rm ${USER_PREFERENCE_INPUT_PATH}/*
   ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -put ${DATA_PATH}/user_preference ${USER_PREFERENCE_INPUT_PATH}/part-00000
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
#####抽取用户画像
#####小区均价/居室面积
#####90%置信度
###############################################
function get_user_figure
{
    sh -x "${BIN_PATH}/user_figure.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "user_figure is success !!!"
    else
        print_log "user_figure is failed !!!"
        exit 1
   fi
   ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -getmerge ${USER_FIGURE_OUTPT_PATH} "${DATA_PATH}/user_figure"
   ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -rm ${USER_FIGURE_OUTPT_PATH}/*
   ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -put ${DATA_PATH}/user_figure ${USER_FIGURE_OUTPT_PATH}/part-00000
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
   cd -
}

#################################################
#####用户个性化房源推荐
###############################################
function get_user_house_recommend
{
    sh -x "${BIN_PATH}/user_house_recommend.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "user_house_recommend is success !!!"
    else
        print_log "user_house_recommend is failed !!!"
        exit 1
   fi
   cd -
}

#################################################
#####房源推荐优化
#####过滤历史带看房源
#####优化小区均价区间
###############################################
function get_recommend_optimize
{
    sh -x "${BIN_PATH}/recommend_optimize.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "recommend_optimize is success !!!"
    else
        print_log "recommend_optimize is failed !!!"
        exit 1
   fi
   cd -
}

#################################################
#####更新mysql数据
###############################################
function update_mysql
{
    cd ./data
    rm recommendation_result
    rm user_house_recommend_part*
    ${GLOBAL_HADOOP_HOME}/bin/hadoop fs -getmerge ${RECOMMEND_OPTIMIZE_OUTPT_PATH} recommendation_result
    cat recommendation_result | python ../lib/process_data.py | split -a 2 -d -l 5000000 - user_house_recommend_part

    HOSTNAME="172.16.6.67"
    PORT="3306"
    USER="house_rc"
    PWD="house_rc213456"
    DBNAME="house_recommendation"
    TABLENAME="recommend_house_itemcf"
    TABLEBAK="recommend_house_itemcf_${RUN_LAST_DAY}"
    OLDTABLE="recommend_house_itemcf_${RUN_THREE_DAY_AGO}"

    rename_sql="alter table ${TABLENAME} rename to ${TABLEBAK}"
    mysql -h${HOSTNAME} -P${PORT} -u${USER} -p${PWD} ${DBNAME} -e "${rename_sql}"
    create_sql="create table ${TABLENAME} like ${TABLEBAK}"
    mysql -h${HOSTNAME} -P${PORT} -u${USER} -p${PWD} ${DBNAME} -e "${create_sql}"
    drop_sql="drop table ${OLDTABLE}"
    mysql -h${HOSTNAME} -P${PORT} -u${USER} -p${PWD} ${DBNAME} -e "${drop_sql}"

    for file_name in `ls user_house_recommend_part*`
    do
        echo "========BEGIN:load data ${file_name}========"
        load_sql="load data local infile '${file_name}' into table ${TABLENAME}(phone,resblock_id,resblock_name,room_cnt,similarity_score)"
        mysql -h${HOSTNAME} -P${PORT} -u${USER} -p${PWD} ${DBNAME} --local-infile=1 -e "${load_sql}"
        echo "======== END :load data ${file_name}========"
    done
    cd -
}

get_extract_data
get_user_preference_filter
get_user_figure
get_user_house_vector
get_house_user_vector
get_house_cosine
get_house_cosine_topN
get_user_house_recommend
get_recommend_optimize
update_mysql
