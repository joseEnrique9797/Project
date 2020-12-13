USE ProjectBD1;

DELIMITER $$
    DROP PROCEDURE IF EXISTS userLog;
    CREATE PROCEDURE userLog (IN userName VARCHAR(200), IN userPassword VARCHAR(200), OUT userId INT, OUT userAdmin BIT, OUT result BIT)
    BEGIN

        IF  ((SELECT COUNT(*) FROM User WHERE var_userName = userName AND var_password = userPassword AND enu_state = "active") = 1) 
            THEN 
                SET @SELECTED = 0;                
                SELECT (SELECT id FROM User WHERE var_userName = userName AND var_password = userPassword LIMIT 1) INTO @SELECTED;                
                INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (@SELECTED, "El usuario ha iniciado Session");                
                SELECT @SELECTED INTO userId;
                SELECT (SELECT bit_admin FROM User WHERE id = @SELECTED) INTO userAdmin;
                SELECT 1 INTO result;
            ELSE 
                SELECT 0 INTO result;
        END IF;
    END $$

DELIMITER ;


DELIMITER $$
    DROP PROCEDURE IF EXISTS userUpdate;
    CREATE PROCEDURE userUpdate (IN userId INT, IN userName VARCHAR(200), IN userPassword VARCHAR(200))
    BEGIN
        UPDATE User SET var_userName = userName, var_password = userPassword, enu_state = "active" WHERE id = userId;
        INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (userId, "Los campos del Usuario han sido actualizados");
    END $$

DELIMITER ;


DELIMITER $$
    DROP PROCEDURE IF EXISTS userChangeState;
    CREATE PROCEDURE userChangeState (IN userId INT)
    BEGIN
        IF  ((SELECT enu_state FROM User WHERE id = userId) = "active") 
            THEN                 
                UPDATE User SET enu_state = "inactive" WHERE id = userId;
            ELSE 
                UPDATE User SET enu_state = "active" WHERE id = userId;
        END IF;

        INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (userId, "El estado del Usuario ha sido actualizado");
    END $$

DELIMITER ;


DELIMITER $$

    DROP PROCEDURE IF EXISTS newDraw;
    CREATE PROCEDURE newDraw (IN userId INT, IN drawName VARCHAR(200), IN drawData JSON, OUT result INT)
    BEGIN
        IF  ((SELECT COUNT(*) FROM Draw WHERE var_name = drawName) = 0) 
            THEN                 
                INSERT INTO Draw (var_name, jso_data) VALUES (drawName, drawData);                
                SELECT (SELECT id FROM Draw ORDER BY id DESC LIMIT 1) INTO result;
                INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (userId, "El usuario ha creado un nuevo dibujo");                
            ELSE 
                SELECT 0 INTO result;
        END IF;
    END $$

DELIMITER ;


DELIMITER $$

    DROP PROCEDURE IF EXISTS changeCanvasConfig;
    CREATE PROCEDURE changeCanvasConfig (IN userId INT, IN penColor VARCHAR(20), IN fillColor VARCHAR(20))
    BEGIN        
        UPDATE canvas_config SET var_pen_color = penColor, var_fill_color = fillColor WHERE id = 1;
        INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (userId, "El usuario ha actualizado la configuracion del pincel");     
    END $$

DELIMITER ;


DELIMITER $$

    DROP PROCEDURE IF EXISTS getCanvasConfig;
    CREATE PROCEDURE getCanvasConfig (OUT Pen VARCHAR(20), OUT Fill VARCHAR(20))
    BEGIN        
        SELECT (SELECT var_pen_color FROM canvas_config WHERE id = 1) INTO Pen;
        SELECT (SELECT var_fill_color FROM canvas_config WHERE id = 1) INTO Pen;  
    END $$

DELIMITER ;

