DROP DATABASE IF EXISTS ProyectBD1;
CREATE DATABASE IF NOT EXISTS ProyectBD1 CHARACTER SET utf8;
USE ProyectBD1;

    

CREATE TABLE IF NOT EXISTS User(
    id INT AUTO_INCREMENT PRIMARY KEY,
    var_userName VARCHAR(200) NOT NULL COMMENT "nombre para el usuario",
    var_password VARCHAR(200) NOT NULL COMMENT "contraseña para el usuario",
    bit_admin bit not null COMMENT "define si el usuario es administrador",
    enu_state ENUM('inactive','active') DEFAULT 'active' COMMENT "Se asigna un estado al usuario para simular el estado de activo y eliminado(inactivo)",
    CONSTRAINT user_nameID UNIQUE(var_userName)
);

CREATE TABLE IF NOT EXISTS Action_type(
    id INT AUTO_INCREMENT PRIMARY KEY,
    var_description VARCHAR(200) COMMENT "Describe el tipo de accion que se registrara en la bitacora."
);

    
CREATE TABLE IF NOT EXISTS Draw(
    id INT AUTO_INCREMENT PRIMARY KEY,
    jso_data JSON COMMENT "Almacenara la informacion correspondiente de la imagen en formato JSON"
);
    
CREATE TABLE IF NOT EXISTS Library(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_action_type INT NOT NULL, 
    int_id_user INT NOT NULL COMMENT "Llave foranea hacia la tabla user",
    int_id_draw INT NOT NULL COMMENT "Llave foranea hacia la tabla draw",
    FOREIGN KEY (int_id_user) REFERENCES User(id),
    FOREIGN KEY (int_id_draw) REFERENCES Draw(id),
    CONSTRAINT id_draw UNIQUE(int_id_draw) COMMENT "Se define como id unico, para evitar que una misma imagen se asigne a varios usuarios."
);

CREATE TABLE IF NOT EXISTS Binnacle(
    id INT AUTO_INCREMENT PRIMARY KEY,
    int_id_user_binn INT NOT NULL COMMENT "Llave foranea hacia la tabla users.",
    int_id_action_type INT NOT NULL COMMENT "Llave foranea hacia la tabla action_type.",
    FOREIGN KEY (int_id_user_binn) REFERENCES User(id),
    FOREIGN KEY (int_id_action_type) REFERENCES Action_type(id)
);

    

    