USE ProjectBD1_Backup;

DELIMITER $$

    DROP PROCEDURE IF EXISTS sp_download $$

    CREATE PROCEDURE sp_download (IN userId INT, IN nameFile VARCHAR(50), OUT draw JSON)

    BEGIN
        SELECT (
            SELECT 
                jso_compressedDraw 
            FROM 
                DrawBackup 
            WHERE 
                (JSON_UNQUOTE(JSON_EXTRACT(jso_compressedDraw,"$.User"))=userId AND 
                JSON_UNQUOTE(JSON_EXTRACT(jso_compressedDraw,"$.FileName"))=nameFile)) 
        INTO 
            draw;
    END $$
DELIMITER ;

--SET @Id = 1;
--SET @Name = "aiudaaaa";
--SET @resultado = "{}";
--CALL sp_download(@Id,@Name,@resultado);
--SELECT @resultado AS "El JSON Descargado es: ";
    