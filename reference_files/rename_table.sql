
# rename table
ALTER TABLE import_mailmerge RENAME TO import_mailMerge;
ALTER TABLE memberpagexref RENAME TO memberPageXref;
ALTER TABLE qb_campaign_serviceitem_mapping RENAME TO qb_campaign_serviceItem_mapping;
ALTER TABLE qb_dts_account_itemmapping RENAME TO qb_dts_account_ItemMapping;
ALTER TABLE qb_fund_serviceitem_mapping RENAME TO qb_fund_serviceItem_mapping;
ALTER TABLE qb_sellingitem_depositaccount_mapping RENAME TO qb_sellingItem_depositAccount_mapping;
ALTER TABLE qb_sellingitem_serviceitem_mapping RENAME TO qb_sellingItem_serviceItem_mapping;
COMMIT;
# rename CO table/view
#SET @table_open_cache = @@table_open_cache; SET GLOBAL table_open_cache = 16384;
#SET @table_definition_cache = @@table_definition_cache; SET GLOBAL table_definition_cache = 16384;

delimiter $$
DROP PROCEDURE IF EXISTS dt_zxb_rename_table$$
CREATE PROCEDURE dt_zxb_rename_table() LANGUAGE SQL MODIFIES SQL DATA  SQL SECURITY  DEFINER
BEGIN

	DECLARE t_name_l VARCHAR(255) DEFAULT NULL;
	DECLARE t_name_u VARCHAR(255) DEFAULT NULL;

	DECLARE done TINYINT DEFAULT 0;
	DECLARE cur CURSOR FOR SELECT tableName FROM cst_custom_object_info;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	
	OPEN cur;
	FETCH cur INTO t_name_u;
	WHILE NOT done DO
		
		
		SET t_name_l = LOWER(t_name_u);
		SET @v_name_l = CONCAT(t_name_l,"_view");
		SET @v_name_u = CONCAT(t_name_u,"_view");

		SET @concat_sql = CONCAT("ALTER TABLE ",t_name_l," RENAME TO ", t_name_u);
		PREPARE concat_sql FROM @concat_sql;
		EXECUTE concat_sql;
		
		SET @concat_sql = CONCAT("CREATE VIEW ",@v_name_u," AS SELECT * FROM ",t_name_u);
		PREPARE concat_sql FROM @concat_sql;
		EXECUTE concat_sql;
		
		SET @concat_sql = CONCAT("DROP VIEW ",@v_name_l);
		PREPARE concat_sql FROM @concat_sql;
		EXECUTE concat_sql;
		
		FETCH cur INTO t_name_u;
		
	END WHILE;

END$$

delimiter ;
CALL dt_zxb_rename_table();
DROP PROCEDURE IF EXISTS dt_zxb_rename_table;
#SET GLOBAL table_open_cache = @table_open_cache;
#SET GLOBAL table_definition_cache = @table_open_cache;

COMMIT;

