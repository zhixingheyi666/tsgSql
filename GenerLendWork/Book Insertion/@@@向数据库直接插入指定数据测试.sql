-- select * from lendwork where loperator = '王_00';
-- -- delete from lendwork where loperator = '王_00';


-- select * from bookclass order by bid desc;

-- 根据查询，inForm大约对应每年的增量，程序中的标志大概是总括登记号
-- select distinct inForm from bookclass;
-- select distinct Ddid from bookclass;
-- select * from bookclass where inForm in (3,4,5);
-- select * from bookclass where inForm in (6);
-- select * from bookclass where inForm in (8);
-- select * from bookclass where Clerk = '王_00'
-- --delete from bookclass where Clerk = '王_00';
-- 写一段语句，插入数据用于增加图书册数，等检查完毕，可以利用约定标记，轻易删除插入的数据
-- 约定插入的图书的Bcid为(# # Bcid必须是Booklist表中存在的，否则会报错),
-- 	bid为06****，EnterDate视情况而定(可以写时间字符串格式，如2018-10-17 08:26:28.297)，
--	price为11，sk为2，inForm与同年的inForm相同,Ddid为NULL,Clerk为王_00
-- 示例:
-- insert into bookclass(Bcid, Bid, State, Clerk, EnterDate, price, sk, inForm) Values('I267/234','060000',0,'王_00','2018-10-17 08:26:28.297',11,2,8);