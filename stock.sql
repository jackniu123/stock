-- create database stock;
use stock;
show databases;
show tables;
-- create table test(col1 int);
select * from test;
-- drop table daily;
-- create table daily(ts_code varchar(255),trade_date varchar(255), _open float,high float, low float, _close float,pre_close float, _change float);
-- create table daily(ts_code varchar(255), trade_date varchar(255), open float, high float, low float, close float, pre_close float, _change float, pct_chg float, vol float, amount float,primary key(ts_code, trade_date));
-- select * from daily;
select count(*) from daily;
show table status like "daily";
SELECT 
table_schema as '数据库',
sum(table_rows) as '记录数',
sum(truncate(data_length/1024/1024, 2)) as '数据容量(MB)',
sum(truncate(index_length/1024/1024, 2)) as '索引容量(MB)',
sum(truncate(DATA_FREE/1024/1024, 2)) as '碎片占用(MB)'
from information_schema.tables
group by table_schema
order by sum(data_length) desc, sum(index_length) desc;

select * from daily limit 10;


