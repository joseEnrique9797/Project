USE ProjectBD1;


DELIMITER $$

    DROP TRIGGER IF EXISTS newUser;

    CREATE TRIGGER newUser AFTER INSERT 
    ON User FOR EACH ROW

    BEGIN        
        INSERT INTO Binnacle (int_id_user_binn, `action`) VALUES (new.id, CONCAT("El usuario: ", new.var_userName, " se ha creado en el sistema"));
    END $$

DELIMITER ;

/*
INSERT INTO User (var_userName,var_password,bit_admin) VALUES ("Lexer Ochoa","aassadma",1);
SELECT * from Binnacle;
/**/