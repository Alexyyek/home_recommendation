#!/bin/bash
function get_data
{
#    hive -e 'select id, district_id, bizcircle_id, name, green_rate, cubage_rate, build_start_date, building_cnt, house_cnt, admin_addr from dw.dw_house_core_resblock_da where pt="20160619000000" and city_id = "11";' > resblock_info.txt
#    hive -e 'select id, name from dw.dw_house_zoning_district_da where pt="20160619000000" and city_id="11";' > district_info.txt
#    hive -e 'select id, name from dw.dw_house_zoning_bizcircle_da where pt="20160619000000" and city_id="11";' > bizcircle_info.txt
#    hive -e 'select resblock_id, resblock_name, trans_price from data_center.bd_rpt_vol_trans_price_month where pt="20160501000000" and city_id="110000" and geography_dim="resblock" and bedroom_amount="-1";' > resblock_price.txt
#    hive -e 'select b.resblock_id, b.image_id, a.image_url from dw.dw_house_entity_image_da a, ods.ods_house_entity_resblock_image_da b where a.pt="20160619000000" and b.pt="20160619000000" and a.city_id="11" and b.city_id="11" and a.id=b.image_id;' > resblock_image.txt
#    hive -e 'select house_pkid, hdic_house_id, total_prices, biz_type, room_cnt, build_area, resblock_id, resblock_name, district_name, bizcircle_name from data_center.dim_merge_house_day where pt="20160622000000" and biz_type="200200000001" and city_id="110000" and (state="200100000001" or state="200100000002");' > house_detail.txt
    hive -e "select house_pkid, total_prices, build_area, room_cnt, parlor_cnt, cookroom_cnt, toilet_cnt, balcony_cnt, resblock_id, resblock_name, district_name, bizcircle_name from data_center.dim_merge_house_day where pt='${RUN_DAY}000000' and biz_type='${BIZ_TYPE}' and city_id='${CITY_ID}';" > data/house_detail/${RUN_DAY}.txt
    hive -e "select id, mobile from ods.ods_uc_user_da where pt='${RUN_DAY}000000';" > data/ucid_mobile/${RUN_DAY}.txt
    hive -e "select uc_id, fav_time, fav_object_id, fav_object_type from data_center.dim_user_fav_day where pt='${RUN_DAY}000000' and fav_time>='2014-06-01' and (fav_object_type='ershoufang' or fav_object_type='resblock');" > data/user_fav/${RUN_DAY}.txt
}

function process_data
{
    awk 'BEGIN{FS="\t";OFS="\t";
        while(getline<"district_info.txt")
            district[$1] = $2;
        while(getline<"bizcircle_info.txt")
            bizcircle[$1] = $2;
        while(getline<"resblock_price.txt")
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
        }' resblock_info.txt
}
get_data
#process_data
