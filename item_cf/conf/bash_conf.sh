export RUN_PATH="/home/work/yangyekang/resblock/resblock_recommend/item_cf"

export BIN_PATH=${RUN_PATH}"/bin"
export DATA_PATH=${RUN_PATH}"/data"
export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
export RUN_DAY=`date +%Y%m%d`
#export RUN_DAY=`date -d"-1 day" +%Y%m%d`
export RUN_LAST_MONTH=`date -d -1"months" +%Y%m`
export RUN_LAST_DAY=`date -d -1"days" +%Y%m%d`
export RUN_THREE_DAY_AGO=`date -d -3"days" +%Y%m%d`

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
export EXTRACT_DATA_OUTPT_PATH='/user/yangyekang/house/resblock_recommend/item_cf/user_preference'

##user figure
export ROOM_THRESHOLD=0.05
export RECENT_DAYS=7
export ONE_RECORD_MARGIN=0.2
export THRESHOLD_NINTY=1.645
export THRESHOLD_NINTY_FIVE=1.96
export USER_FIGURE_INPUT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_preference_filter"
export USER_FIGURE_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_figure"

##user preference filter
export FILTER_RATIO=0.01
export USER_PREFERENCE_INPUT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_preference"
export USER_PREFERENCE_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_preference_filter"

##user house vector
export USER_HOUSE_INPUT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_preference_filter"
export USER_HOUSE_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_house_vector"

##house user vector
export HOUSE_USER_INPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_preference_filter"
export HOUSE_USER_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/house_user_vector"

##house cosine cal
export HOUSE_COSINE_INPUT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_house_vector"
export HOUSE_COSINE_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/house_cosine"

##house cosine topN
export TOPN=100
export HOUSE_COSINE_TOP_INPUT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/house_cosine"
export HOUSE_COSINE_TOP_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/house_cosine_topN"

##user house recommend
export TOP_NUM=50
export USER_HOUSE_RECOMMEND_INPUT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_house_vector"
export USER_HOUSE_RECOMMEND_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_house_recommend/${RUN_DAY}"

##recommend optimize
export RECOMMEND_OPTIMIZE_INPUT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/user_house_recommend/${RUN_DAY}"
export RECOMMEND_OPTIMIZE_OUTPT_PATH="/user/yangyekang/house/resblock_recommend/item_cf/recommend_optimize/${RUN_DAY}"

##third part data
export DIM_MERGE_HOUSE_DAY="/user/yangyekang/online_data/tools/dim_merge_house_day"
export UCID_MOBILE="/user/songxin/tools/ucid_mobile/${RUN_LAST_DAY}.txt"
export SPIDER="/user/songxin/tools/spider/spider.txt"
export RESBLOCK_PRICE="/user/hive/warehouse/data_center.db/bj_bd_rpt_vol_resblock_trans_price_month/pt=${RUN_LAST_MONTH}01000000/000000_0"
