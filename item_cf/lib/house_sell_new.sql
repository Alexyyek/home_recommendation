--在售房源信息
SELECT
t1.hdic_resblock_id,
t2.house_pkid,
t1.house_title,
t1.price_trans,
t1.house_area,
t1.frame_hall_num,
t1.frame_bedroom_num,
t1.price_trans / t1.house_area,
t1.frame_structure,
concat(t1.floor_num, '/', t1.floor_total),
t1.frame_orientation,
t1.tags
FROM
(
SELECT
hdic_resblock_id,
house_code,
hdic_house_id,    --楼盘字典房间ID
house_title,      --房源标题
price_trans,      --挂牌价
house_area,       --房屋面积
frame_hall_num,   --厅数量
frame_bedroom_num,--卧室数量
frame_structure,  --户型
floor_num,        --所在楼层
floor_total,      --总楼层
frame_orientation,--朝向
tags              --房屋标签
FROM
data_center.house_sell_new
WHERE
pt='${hiveconf:pt}'
AND hdic_city_id='${hiveconf:city_id}'
AND bit_status&32768!=0 and bit_status&64!=0
) AS t1
JOIN
(
SELECT
house_pkid
FROM
data_center.dim_merge_house_day
WHERE
pt='${hiveconf:pt}'
AND city_id='${hiveconf:city_id}'
AND state=200100000001
) AS t2
ON substr(t1.house_code, -8) = substr(t2.house_pkid, -8)
;
