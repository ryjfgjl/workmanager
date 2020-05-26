#########################################################################
# add_rowid
DROP PROCEDURE IF EXISTS add_rowid;
delimiter //
CREATE PROCEDURE add_rowid()
	BEGIN
		DECLARE tname VARCHAR(255);
		DECLARE done INT DEFAULT FALSE;
		DECLARE con_sql VARCHAR(255);	
		DECLARE cur CURSOR FOR SELECT TABLE_NAME FROM information_schema.`TABLES` a WHERE a.TABLE_SCHEMA = DATABASE() AND TABLE_NAME LIKE 'z|_excel|_%' ESCAPE '|';
		DECLARE CONTINUE HANDLER FOR NOT found SET done = TRUE;

		OPEN cur;
		FETCH cur INTO tname;
		
		WHILE NOT done DO
			SET @id = 0;
			SET @tname = tname;
			SET @con_sql = CONCAT('ALTER TABLE ',@tname,' ADD COLUMN neon_rowId INT DEFAULT NULL');
			PREPARE exec_sql FROM @con_sql;
			EXECUTE exec_sql;
			SET @con_sql = CONCAT('UPDATE ',@tname,' SET neon_rowId = (@id := @id + 1)');
			PREPARE exec_sql FROM @con_sql;
			EXECUTE exec_sql;
			FETCH cur INTO tname;
			SET @id = 0;
		END WHILE;
		DEALLOCATE PREPARE exec_sql;
		CLOSE cur;
	END;
//
delimiter ;
CALL add_rowid;
DROP PROCEDURE IF EXISTS add_rowid;
#########################################################################
COMMIT;