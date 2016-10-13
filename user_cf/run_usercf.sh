#!/bin/bash
day=`date -d"-1 day" +%Y%m%d`
#source "./conf/conf.sh" ${day}
source "./conf/conf.sh" 20160717
source "./lib/common_lib.sh"

#################################################
#####计算用户行为变量
###############################################
function get_user_vector
{
    cd ./modules/user_vector
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "user_vector is success !!!"
    else
        print_log "user_vector is failed !!!"
        exit 1
    fi
    cd -
}

#################################################
#####用户行为变量清洗
###############################################
function get_user_vector_clean
{
    cd ./modules/user_vector_clean
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "user_vector_clean is success !!!"
    else
        print_log "user_vector_clean is failed !!!"
        exit 1
    fi
    cd -
    ${HADOOP_HOME}/bin/hadoop fs -cat ${CLEAN_USER_VECTOR_OUTPUT_PATH}/* > ${LOCAL_CLEAN_USER_VECTOR_FILE_PATH}
    LOCAL_CLEAN_VECTOR_DIR_PATH=`dirname ${LOCAL_CLEAN_USER_VECTOR_FILE_PATH}`
    HDFS_CLEAN_VECTOR_DIR_PATH=`dirname ${HDFS_CLEAN_USER_VECTOR_FILE_PATH}`
    rm ${LOCAL_CLEAN_VECTOR_DIR_PATH}/${DEAD_DAY}.txt
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_CLEAN_USER_VECTOR_FILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_CLEAN_USER_VECTOR_FILE_PATH} ${HDFS_CLEAN_USER_VECTOR_FILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_CLEAN_VECTOR_DIR_PATH}/${DEAD_DAY}.txt
}

################################################
####建立倒排
##############################################
function get_inverse_index
{
    cd ./modules/inverse_index
    sh -x run.sh 
    if [[ $? == 0 ]]
    then
        print_log "inverse_index is success !!!"
    else
        print_log "inverse_index is failed !!!"
        exit 1
    fi
    cd -
}

################################################
####分批计算用户相似性权重
##############################################
function get_user_similarity_seg
{
    cd ./modules/user_similarity_seg
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "user_similarity_seg is success !!!"
    else
        print_log "user_similarity_seg is failed !!!"
        exit 1
    fi
    cd -
}

################################################
####统计用户相似性权重
##############################################
function get_user_similarity_merge
{
    cd ./modules/user_similarity_merge
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "user_similarity_merge is success !!!"
    else
        print_log "user_similarity_merge is failed !!!"
        exit 1
    fi
    cd -
}

#############################################################
####用户相似性汇总
#############################################################
function get_user_similarity_total
{
    cd ./modules/user_similarity_total
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "user_similarity_total is success !!!!"
    else
        print_log "user_similarity_total is failed !!!!"
        exit 1
    fi
    cd -
}
################################################
####分片计算计算top N最近用户
##############################################
function get_top_N_similar_user_seg
{
    cd ./modules/top_N_similar_user_seg
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "top_N_similar_user is success !!!!"-
    else
        print_log "top_N_similar_user is failed !!!"
        exit 1
    fi
    cd -
}


################################################
####计算top N最近用户
##############################################
function get_top_N_similar_user_total
{
    cd ./modules/top_N_similar_user_total
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "top_N_similar_user is success !!!!"-
    else
        print_log "top_N_similar_user is failed !!!"
        exit 1
    fi
    cd -
}

################################################
####计算得到用户带看房源集合
##############################################
function get_user_touring_set
{
    cd ./modules/user_touring_set
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "user_touring_set is success !!!!"-
    else
        print_log "user_touring_set is failed !!!"
        exit 1
    fi
    cd -
    ${HADOOP_HOME}/bin/hadoop fs -cat ${USER_TOURING_OUTPUT_PATH}/* > ${LOCAL_USER_TOURING_SET_FILE_PATH}
    LOCAL_TOURING_DIR_PATH=`dirname ${LOCAL_USER_TOURING_SET_FILE_PATH}`
    HDFS_TOURING_DIR_PATH=`dirname ${HDFS_USER_TOURING_SET_FILE_PATH}`
    rm ${LOCAL_TOURING_DIR_PATH}/${DEAD_DAY}.txt
    ${HADOOP_HOME}/bin/hadoop fs -put ${LOCAL_USER_TOURING_SET_FILE_PATH} ${HDFS_USER_TOURING_SET_FILE_PATH}
    ${HADOOP_HOME}/bin/hadoop fs -rm ${HDFS_TOURING_DIR_PATH}/${DEAD_DAY}.txt
}

##########################################################################################
####计算推荐房源
##########################################################################################
function get_recommendation
{
    cd ./modules/recommendation
    sh -x run.sh
    if [[ $? == 0 ]]
    then
        print_log "recommendation is success !!!!"-
    else
        print_log "recommendation is failed !!!"
        exit 1
    fi
    cd -
}

##############################################
#更新mysql数据库
#############################################
function update_mysql
{
    cd ./data
    rm -rf recommendation_result
    ${HADOOP_HOME}/bin/hadoop fs -get /user/songxin/unified_recommendation/recommendation_result/${RUN_DAY} recommendation_result
    rm recommendation_result.x*
    cat recommendation_result/* | python ../lib/recommendation_filter.py mysql_resblock_data/resblock_bedroom_price.txt user_vector_clean/* |python ../lib/process_data.py | split -l 2000000 - recommendation_result.x
    TABLE_NAME="recommend_house_user_cf_${RUN_DAY}"
    mysql -h 172.30.17.1 -P 3306 -uroot -proot --local-infile=1 -e "create table house_recommendation.${TABLE_NAME} like house_recommendation.recommend_house_usercf;"
    for file_name in `ls recommendation_result.x*`
    do
        echo "========BEGIN:load data ${file_name}========"
        mysql -h 172.30.17.1 -P 3306 -uroot -proot --local-infile=1 -e "load data local infile '${file_name}' into table house_recommendation.${TABLE_NAME}"
        echo "======== END :load data ${file_name}========"
    done
    cd -
}

#get_user_vector
#get_user_vector_clean
#get_inverse_index
#get_user_similarity_seg
#get_user_similarity_merge
#get_user_similarity_total
#get_top_N_similar_user_seg
#get_top_N_similar_user_total
#get_user_touring_set
#get_recommendation
update_mysql
