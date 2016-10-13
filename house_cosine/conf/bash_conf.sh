export RUN_PATH="/home/work/yangyekang/resblock/resblock_recommend/house_cosine"

export BIN_PATH=${RUN_PATH}"/bin"
export DATA_PATH=${RUN_PATH}"/data"
export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
export RUN_DAY=`date +%Y%m%d`
export RUN_LAST_MONTH=`date -d -1"months" +%Y%m`
export RUN_LAST_DAY=`date -d -1"days" +%Y%m%d`

##extract data
export Alpha=0.0063
export ONLINE_CODE='online'
export OFFLINE_CODE='offline'
export ONLINE_BROWSE_WEIGHT=1
export ONLINE_FAV_WEGIHT=8
export OFFLINE_TOURING_WEIGHT=10
export OFFLINE_CONTRACT_WEIGHT=50
export ONLINE_OFFLINE_THRESHOLD=5
export ONE_ROOM_INTERVAL=30,50,80
export TWO_ROOM_INTERVAL=50,80,130
export THREE_ROOM_INTERVAL=75,90,140,300
export PC_PATH='/user/songxin/new_unified_user_behaviour/pc'
export MOBILE_PATH='/user/songxin/new_unified_user_behaviour/mobile'
export ONLINE_PATH='/user/songxin/new_unified_user_behaviour/ual_behaviour'
export OFFLINE_PATH="/user/songxin/new_unified_user_behaviour/offline_data/${RUN_LAST_DAY}"
export FAV_PATH='/user/yangyekang/online_data/fav'
export EXTRACT_DATA_OUTPT_PATH='/user/yangyekang/house/house_cosine/user_preference'

##user preference filter
export FILTER_RATIO=0.005
export USER_PREFERENCE_INPUT_PATH="/user/yangyekang/house/house_cosine/user_preference"
export USER_PREFERENCE_OUTPT_PATH="/user/yangyekang/house/house_cosine/user_preference_filter"

##user house vector
export USER_HOUSE_INPUT_PATH="/user/yangyekang/house/house_cosine/user_preference_filter"
export USER_HOUSE_OUTPT_PATH="/user/yangyekang/house/house_cosine/user_house_vector"

##house user vector
export HOUSE_USER_INPT_PATH="/user/yangyekang/house/house_cosine/user_preference_filter"
export HOUSE_USER_OUTPT_PATH="/user/yangyekang/house/house_cosine/house_user_vector"

##house cosine cal
export HOUSE_COSINE_INPUT_PATH="/user/yangyekang/house/house_cosine/user_house_vector"
export HOUSE_COSINE_OUTPT_PATH="/user/yangyekang/house/house_cosine/house_cosine"

##house cosine topN
export TOPN=50
export HOUSE_COSINE_TOP_INPUT_PATH="/user/yangyekang/house/house_cosine/house_cosine"
export HOUSE_COSINE_TOP_OUTPT_PATH="/user/yangyekang/house/house_cosine/house_cosine_topN/${RUN_DAY}"

##updata redis
export host_idc=m11036.zeus.redis.ljnode.com
export port_idc=11036
export host_aws=m11036.ares.redis.ljnode.com
export port_aws=11036
export host_test=172.30.0.20
export port_test=6379
export expire=2592000

##third part data
export DIM_MERGE_HOUSE_DAY="/user/yangyekang/online_data/tools/dim_merge_house_day_city"
export SPIDER="/user/songxin/tools/spider/spider.txt"

