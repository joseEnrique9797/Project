USE ProjectBD1;

DELIMITER $$
    DROP PROCEDURE IF EXISTS userLog;
    CREATE PROCEDURE userLog (IN userName VARCHAR(200), IN userPassword VARCHAR(200), OUT result BIT)
    BEGIN

        IF  ((SELECT COUNT(*) FROM User WHERE var_userName = userName AND var_password = userPassword) = 1) 
            THEN 
                SET @SELECTED = 0;                
                SELECT (SELECT id FROM User WHERE var_userName = userName AND var_password = userPassword LIMIT 1) INTO @SELECTED;                
                INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (@SELECTED, "El usuario ha iniciado Session");                
                SELECT 1 INTO result;
            ELSE 
                SELECT 0 INTO result;
        END IF;
    END $$

DELIMITER ;


DELIMITER $$

    DROP PROCEDURE IF EXISTS newDraw;
    CREATE PROCEDURE newDraw (IN userId INT, IN drawName VARCHAR(200), IN drawData JSON, OUT result BIT)
    BEGIN
        IF  ((SELECT COUNT(*) FROM Draw WHERE var_name = drawName) = 0) 
            THEN                 
                INSERT INTO Draw (var_name, jso_data) VALUES (drawName, drawData);                
                INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (userId, "El usuario ha creado un nuevo dibujo");                
                SELECT 1 INTO result;
            ELSE 
                SELECT 0 INTO result;
        END IF;
    END $$

DELIMITER ;


DELIMITER $$

    DROP PROCEDURE IF EXISTS addCanvasConfig;
    CREATE PROCEDURE addCanvasConfig (IN userId INT, IN penColor VARCHAR(20), IN fillColor VARCHAR(20))
    BEGIN        
        INSERT INTO canvas_config (var_pen_color, var_fill_color) VALUES (penColor, fillColor);                
        INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (userId, "El usuario ha creado una nueva configuracion del pincel");     
    END $$

DELIMITER ;





INSERT INTO User (var_userName,var_password,bit_admin) VALUES ("Andres Zuniga","cusadmin",1);

SET @resultado = 0;
CALL userLog("Andres Zuniga","cusadmin", @resultado);
CALL newDraw(2,"fakePaint2",'{"name":"myDibujo"}', @resultado);

SELECT * from Binnacle;