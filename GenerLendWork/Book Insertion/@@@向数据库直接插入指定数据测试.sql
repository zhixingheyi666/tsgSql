-- select * from lendwork where loperator = '��_00';
-- -- delete from lendwork where loperator = '��_00';


-- select * from bookclass order by bid desc;

-- ���ݲ�ѯ��inForm��Լ��Ӧÿ��������������еı�־����������ǼǺ�
-- select distinct inForm from bookclass;
-- select distinct Ddid from bookclass;
-- select * from bookclass where inForm in (3,4,5);
-- select * from bookclass where inForm in (6);
-- select * from bookclass where inForm in (8);
-- select * from bookclass where Clerk = '��_00'
-- --delete from bookclass where Clerk = '��_00';
-- дһ����䣬����������������ͼ��������ȼ����ϣ���������Լ����ǣ�����ɾ�����������
-- Լ�������ͼ���BcidΪ(# # Bcid������Booklist���д��ڵģ�����ᱨ��),
-- 	bidΪ06****��EnterDate���������(����дʱ���ַ�����ʽ����2018-10-17 08:26:28.297)��
--	priceΪ11��skΪ2��inForm��ͬ���inForm��ͬ,DdidΪNULL,ClerkΪ��_00
-- ʾ��:
-- insert into bookclass(Bcid, Bid, State, Clerk, EnterDate, price, sk, inForm) Values('I267/234','060000',0,'��_00','2018-10-17 08:26:28.297',11,2,8);