#!/bin/bash
RUN_DAY=`date -d"-1 day" +%Y%m%d`
RUN_MONTH=`date -d"-1 month" +%Y%m01`
function get_data
{
    hive -e "select id, district_id, bizcircle_id, name, green_rate, cubage_rate, build_start_date, building_cnt, house_cnt, admin_addr from dw.dw_house_core_resblock_da where pt='${RUN_DAY}000000' and city_id = '11';" > ./data/mysql_resblock_data/resblock_info.txt
    hive -e "select id, name from dw.dw_house_zoning_district_da where pt='${RUN_DAY}000000' and city_id='11';" > ./data/mysql_resblock_data/district_info.txt
    hive -e "select id, name from dw.dw_house_zoning_bizcircle_da where pt='${RUN_DAY}000000' and city_id='11';" > ./data/mysql_resblock_data/bizcircle_info.txt
    hive -e "select resblock_id, resblock_name, trans_price from data_center.bd_rpt_vol_trans_price_month where pt='${RUN_MONTH}000000' and city_id='110000' and geography_dim='resblock' and bedroom_amount='-1';" > ./data/mysql_resblock_data/resblock_price.txt
    hive -e "select resblock_id, resblock_name, bedoom_amount, trans_price from data_center.bd_rpt_vol_trans_price_month where pt='${RUN_MONTH}000000' and city_id='110000' and geography_dim='resblock' and bedroom_amount>='0';" > ./data/mysql_resblock_data/resblock_bedroom_price.txt
    hive -e "select b.resblock_id, b.image_id, a.image_url from dw.dw_house_entity_image_da a, ods.ods_house_entity_resblock_image_da b where a.pt='${RUN_DAY}000000' and b.pt='${RUN_DAY}000000' and a.city_id='11' and b.city_id='11' and a.id=b.image_id;" > ./data/mysql_resblock_data/resblock_image.txt
}

function process_data
{
    awk 'BEGIN{FS="\t";OFS="\t";
        while(getline<"./data/mysql_resblock_data/district_info.txt")
            district[$1] = $2;
        while(getline<"./data/mysql_resblock_data/bizcircle_info.txt")
            bizcircle[$1] = $2;
        while(getline<"./data/mysql_resblock_data/resblock_price.txt")
            price[$1] = $3;
        }
        {
            resblock_id = $1;
            district_name = district[$2];
            bizcircle_name = bizcircle[$3];
            resblock_name = $4;
            if($5 == "-1")
                green_rate = "暂无信息";
            else
                green_rate = $5;

            if($6 == "-1")
                cubage_rate = "暂无信息";
            else
                cubage_rate = $6;

            if($7 ~ /^1000/)
                build_year = "暂无信息";
            else
                build_year = substr($7, 1, 4);

            building_cnt = $8;
            house_cnt = $9;
            admin_addr = $10;

            if($1 in price)
                resblock_price = price[$1];
            else
                resblock_price = "暂无信息";

            print resblock_id, district_name, bizcircle_name, resblock_name, resblock_price, green_rate, cubage_rate, build_year, building_cnt, house_cnt, admin_addr;
        }' ./data/mysql_resblock_data/resblock_info.txt > ./data/mysql_resblock_data/resblock_detail.txt
}

function update_mysql
{
    mysql -h 172.30.17.1 -P 3306 -uroot -proot -e 'delete from house_recommendation.resblock_detail;'
    mysql -h 172.30.17.1 -P 3306 -uroot -proot --local-infile=1 -e 'load data local infile "./data/mysql_resblock_data/resblock_detail.txt" into table house_recommendation.resblock_detail;'

    mysql -h 172.30.17.1 -P 3306 -uroot -proot -e 'delete from house_recommendation.resblock_image;'
    mysql -h 172.30.17.1 -P 3306 -uroot -proot --local-infile=1 -e 'load data local infile "./data/mysql_resblock_data/resblock_image.txt" into table house_recommendation.resblock_image;'
}

get_data
process_data
#update_mysql
