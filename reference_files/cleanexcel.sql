#########################################################################
# add dtrowId
# add dtLinkingId
DROP PROCEDURE IF EXISTS dt_zxb_add_rowid;
delimiter //
CREATE PROCEDURE dt_zxb_add_rowid()
	BEGIN
		DECLARE tname VARCHAR(255);
		DECLARE done INT DEFAULT FALSE;
		DECLARE con_sql VARCHAR(255);	
		DECLARE cur CURSOR FOR SELECT TABLE_NAME FROM information_schema.`TABLES` a WHERE a.TABLE_SCHEMA = DATABASE() AND TABLE_NAME LIKE 'z|_excel|_%' ESCAPE '|'
		AND TABLE_NAME NOT IN(SELECT TABLE_NAME FROM information_schema.COLUMNS a WHERE a.TABLE_SCHEMA = DATABASE() AND COLUMN_NAME = 'dtrowId');
		DECLARE CONTINUE HANDLER FOR NOT found SET done = TRUE;

		OPEN cur;
		FETCH cur INTO tname;
		
		WHILE NOT done DO
			SET @id = 0;
			SET @tname = tname;
			SET @nickname = SUBSTRING_INDEX(SUBSTRING_INDEX(@tname,'_',3),'_',-1);
			SET @con_sql = CONCAT('ALTER TABLE ',@tname,' ADD COLUMN dtrowId INT DEFAULT NULL, ADD COLUMN dtLinkingId varchar(100) DEFAULT NULL, ADD COLUMN tableName varchar(64) DEFAULT NULL');
			PREPARE exec_sql FROM @con_sql;
			EXECUTE exec_sql;
			SET @con_sql = CONCAT('UPDATE ',@tname,' SET dtrowId = (@id := @id + 1), dtLinkingId = CONCAT(dtrowId,"_",@nickname), tableName = @tname');
			PREPARE exec_sql FROM @con_sql;
			EXECUTE exec_sql;
			SET @con_sql = CONCAT('ALTER TABLE ',@tname,' ADD PRIMARY KEY(dtrowId)');
			PREPARE exec_sql FROM @con_sql;
			EXECUTE exec_sql;

			FETCH cur INTO tname;
			SET @id = 0;
		END WHILE;
		CLOSE cur;
	END;
//
delimiter ;
CALL dt_zxb_add_rowid;
DROP PROCEDURE IF EXISTS dt_zxb_add_rowid;
#########################################################################
COMMIT;