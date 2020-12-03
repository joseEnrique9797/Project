DROP DATABASE IF EXISTS ProyectBD1;
CREATE DATABASE IF NOT EXISTS ProyectBD1 CHARACTER SET utf8;
USE ProyectBD1;

    

CREATE TABLE IF NOT EXISTS User(
    id INT AUTO_INCREMENT PRIMARY KEY,
    var_nickName VARCHAR(200) NOT NULL COMMENT "nombre para el usuario",
    var_password VARCHAR(200) NOT NULL COMMENT "contraseña para el usuario",
    bit_admin bit not null COMMENT "define si el usuario es administrador",
    enu_state ENUM('draft','done') DEFAULT 'done'
);

CREATE TABLE IF NOT EXISTS Action_type(
    id INT AUTO_INCREMENT PRIMARY KEY,
    var_description VARCHAR(200)
);

    
CREATE TABLE IF NOT EXISTS Draw(
    id INT AUTO_INCREMENT PRIMARY KEY,
    jso_data JSON
);
    
CREATE TABLE IF NOT EXISTS Library(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_action_type INT NOT NULL,
    int_id_user INT NOT NULL,
    int_id_draw INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    FOREIGN KEY (int_id_user) REFERENCES User(id),
    FOREIGN KEY (int_id_draw) REFERENCES Draw(id)
);

CREATE TABLE IF NOT EXISTS Binnacle(
    id INT AUTO_INCREMENT PRIMARY KEY,
    int_id_user_binn INT NOT NULL,
    int_id_action_type INT NOT NULL,
    FOREIGN KEY (int_id_user_binn) REFERENCES User(id),
    FOREIGN KEY (int_id_action_type) REFERENCES Action_type(id)
);

    

    