DELIMITER $$
DROP PROCEDURE IF EXISTS lke_export;
CREATE PROCEDURE lke_export()
BEGIN
	DECLARE done INT DEFAULT FALSE;
	DECLARE tableName TEXT DEFAULT "";
	
	DECLARE cursor_tables CURSOR FOR
	SELECT table_name
	FROM information_schema.tables
	WHERE
		table_schema = DATABASE()
		AND table_type = 'BASE TABLE'
	ORDER BY table_name;
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	SET SESSION group_concat_max_len = @@max_allowed_packet;
	-- buffer to be exported to file
	
	OPEN cursor_tables;

	SELECT 'START TRANSACTION;';
	
	getTables: LOOP
		
		FETCH cursor_tables INTO tableName;
		IF done THEN 
			LEAVE getTables;
		END IF;
		
		-- export single line CREATE TABLE statement
		SELECT CONCAT(
			'CREATE TABLE ',
			'`',
			tableName,
			'` (',
			GROUP_CONCAT(CONCAT('`', column_name, '` ', column_type) SEPARATOR ','),
			');'
		)
		FROM
			information_schema.columns
		WHERE
			table_schema = DATABASE()
			AND table_name = tableName
		ORDER BY ordinal_position;
		
		-- dynamic building of value's list for the INSERT INTO statement
		SELECT
			GROUP_CONCAT(
				CONCAT(
					-- manage null values
					'IFNULL(',
					CASE
						WHEN NOT collation_name IS NULL THEN
							-- value is a string: add quotes and replace eventual \n to keep single line instruction
							CONCAT(
								'\n\t\tCASE WHEN INSTR(`', column_name, '`, ''\\n'') > 0',
								'\n\t\t\tTHEN CONCAT(''REPLACE('''''', REPLACE(REPLACE(', CONCAT('`', column_name, '`'), ', ''\\n'', ''\\\\n''), '''''''', ''''''''''''), '''''',''''\\\\n'''',char(10))'')',
								'\n\t\t\tELSE CONCAT('''''''', REPLACE(', CONCAT('`', column_name, '`'), ', '''''''', ''''''''''''), '''''''')',
								'\n\t\tEND'
							)
						WHEN data_type = 'datetime' or data_type = 'date' THEN
							-- date/datime: add quotes
							CONCAT('CONCAT('''''''',', CONCAT('`', column_name, '`'), ','''''''')')
						ELSE
							-- other types: no quotes needed
							CONCAT('`', column_name, '`')
							
					END,
					', ''null'')'
				)
				SEPARATOR ', '','',\n\t'
			)
		INTO @values
		FROM
			information_schema.columns
		WHERE
			table_schema = DATABASE()
			AND table_name = tableName
		ORDER BY ordinal_position;

		-- SELECT @values; -- DEBUG
		
		-- dynamic building of the INSERT INTO statement
		SET @insert_statement = CONCAT('CONCAT(''INSERT INTO `', tableName, '` VALUES ('',\n\t', @values , ',\n'');'')');
		-- export single line INSERT INTO statement for each line in the table
		SET @q1 = CONCAT('SELECT\n\n', @insert_statement, '\n\nFROM `', tableName, '`;');
		
		-- SELECT @q1; -- DEBUG
		PREPARE stmt FROM @q1;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
	
	END LOOP getTables;
	CLOSE cursor_tables;

	SELECT 'COMMIT;';
END$$
DELIMITER ;
