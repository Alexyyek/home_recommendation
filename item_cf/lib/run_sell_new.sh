#!/bin/sh
#coding=utf-8

pt=`date -d -1"days" +%Y%m%d000000`
city_id=110000

hive -hiveconf pt=${pt} -hiveconf city_id=${city_id} -f house_sell_new.sql > ../data/house_sell_new
